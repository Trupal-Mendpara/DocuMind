import os
import uuid
import streamlit as st
from dotenv import load_dotenv
from streamlit_mic_recorder import speech_to_text

from core.llm import load_llm
from core.vectorstore import create_vectorstore
from services.document_loader import extract_text_from_pdf, extract_text_from_image
from services.file_utils import save_uploaded_file, cleanup_file
from chains import get_rag_chain

# ============================================================
# Config
# ============================================================
load_dotenv()
st.set_page_config("📄 DocuMind", "🧠", layout="wide")
st.title("📑 DocuMind")

# ============================================================
# Session State
# ============================================================
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "text" not in st.session_state:
    st.session_state.text = ""

if "vectordb" not in st.session_state:
    st.session_state.vectordb = None

CHROMA_DIR = f"chroma_db/{st.session_state.session_id}"

# ============================================================
# Sidebar
# ============================================================
mode = st.sidebar.radio(
    "Select Mode",
    ["RAG", "Summarization", "Questionnaire Generator"]
)

if st.sidebar.button("🔁 Clear All"):
    st.session_state.clear()
    st.rerun()

# ============================================================
# Upload
# ============================================================
files = st.file_uploader(
    "Upload PDF or Images",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if files and not st.session_state.text:
    combined = ""
    for f in files:
        path = save_uploaded_file(f)
        try:
            if f.name.lower().endswith(".pdf"):
                combined += extract_text_from_pdf(path)
            else:
                combined += extract_text_from_image(path)
        finally:
            cleanup_file(path)

    st.session_state.text = combined
    st.success("✅ Text extraction completed")

text = st.session_state.text
llm = load_llm()

# ============================================================
# RAG MODE
# ============================================================
if mode == "RAG" and text:
    if st.session_state.vectordb is None:
        with st.spinner("Building vector store..."):
            st.session_state.vectordb = create_vectorstore(text, CHROMA_DIR)

    retriever = st.session_state.vectordb.as_retriever(search_kwargs={"k": 3})
    qa = get_rag_chain(llm, retriever)

    st.subheader("💬 Ask Your Document")

    typed = st.text_input("Ask a question")
    spoken = speech_to_text(
        language="en",
        start_prompt="🎙️ Start",
        stop_prompt="🛑 Stop",
        use_container_width=True
    )

    query = spoken or typed

    if query:
        with st.spinner("Thinking..."):
            result = qa({"query": query})

        st.markdown("### 🧠 Answer")
        st.write(result["result"])

        with st.expander("📚 Source Chunks"):
            for i, doc in enumerate(result["source_documents"], 1):
                st.markdown(f"**Chunk {i}**")
                st.write(doc.page_content)

# ============================================================
# SUMMARIZATION
# ============================================================
elif mode == "Summarization" and text:
    st.subheader("📝 Summary")
    st.write(llm.invoke(f"Summarize this:\n{text}").content)

# ============================================================
# QUESTIONNAIRE
# ============================================================
elif mode == "Questionnaire Generator" and text:
    n = st.number_input("Number of questions", 1, 20, 5)

    prompt = f"""
    Generate {n} questions from the text.
    Provide short answers using only the text.

    Format:
    1. Question:
       Answer:

    Text:
    {text}
    """

    with st.spinner("Generating..."):
        res = llm.invoke(prompt)

    st.text_area("Questions", res.content, height=400)

else:
    st.info("📂 Upload files to start")
