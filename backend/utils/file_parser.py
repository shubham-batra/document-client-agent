import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document


def parse_pdf(uploaded_file) -> list[Document]:
    """
    Saves a Streamlit uploaded file to a temporary location, 
    loads it using PyPDFLoader, and returns a list of Documents.
    """
    # 1. Create a temporary file with a .pdf suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        # 2. Write the contents of the uploaded file to the temp file
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        # 3. Load the PDF using the file path
        loader = PyPDFLoader(tmp_file_path)
        documents = loader.load()
        return documents
    finally:
        # 4. Clean up: remove the file from disk after loading
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)