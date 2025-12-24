from langchain_community.document_loaders import PyPDFLoader
from doctr.io import DocumentFile
from core.ocr import load_ocr_model

def extract_text_from_pdf(path):
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    return "\n".join(p.page_content for p in pages)

def extract_text_from_image(path):
    model = load_ocr_model()
    doc = DocumentFile.from_images(path)
    result = model(doc).export()

    text = ""
    for page in result["pages"]:
        for block in page["blocks"]:
            for line in block["lines"]:
                text += " ".join(w["value"] for w in line["words"]) + "\n"
    return text
