# DocuMind 📄🧠

**DocuMind** is an AI-powered document assistant designed to help users interact with their documents intelligently. Built with Streamlit and LangChain, it uses advanced RAG (Retrieval-Augmented Generation) to answer questions based on your uploaded files (PDFs, Images, etc.).

## 🚀 Features

* **Document Q&A:** Chat with your documents to extract summaries, insights, and specific details.
* **OCR Integration:** Supports optical character recognition to read scanned documents and images.
* **Vector Search:** Uses ChromaDB for efficient semantic search within your documents.
* **Interactive UI:** Clean and responsive interface built with Streamlit.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **LLM Framework:** [LangChain](https://www.langchain.com/)
* **Vector Store:** [ChromaDB](https://www.trychroma.com/)
* **Package Manager:** [uv](https://github.com/astral-sh/uv) (for fast Python management)

## 📂 Project Structure

```text
DocuMind/
├── core/               # Core logic (LLM config, OCR, VectorStore)
├── services/           # Helper services (File loaders, Utils)
├── chains.py           # LangChain chains and prompt logic
├── app.py              # Main Streamlit application entry point
├── packages.txt        # System dependencies (for Hugging Face)
├── requirements.txt    # Python dependencies
└── .env                # API keys (Not uploaded to GitHub)
```