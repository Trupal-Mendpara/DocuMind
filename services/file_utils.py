import tempfile
import os

def save_uploaded_file(file):
    suffix = file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(file.read())
        return tmp.name

def cleanup_file(path):
    if os.path.exists(path):
        os.remove(path)
