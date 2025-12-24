from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.llm import load_embeddings

def create_vectorstore(text, persist_dir):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = splitter.split_text(text)

    return Chroma.from_texts(
        chunks,
        load_embeddings(),
        persist_directory=persist_dir
    )
