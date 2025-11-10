import os
from PyPDF2 import PdfReader
import docx
import config
import pytesseract 
from pdf2image import convert_from_path


def allowed_file(filename):
    """ Check if the uploaded file has a valid extension """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def extract_text(file_path):
    """Extract text from uploaded files (.pdf, .docx, .txt), including scanned PDFs"""
    ext = file_path.rsplit('.', 1)[1].lower()
    text = ""

    try:
        if ext == 'txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()

        elif ext == 'pdf':
            # Try normal PDF text extraction
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            # If no text found, fallback to OCR (scanned PDF)
            if not text.strip():
                pages = convert_from_path(file_path)
                for page in pages:
                    text += pytesseract.image_to_string(page) + "\n"

        elif ext in ('docx', 'doc'):
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])

        else:
            raise ValueError("Unsupported file type")

    except Exception as e:
        print(f"[ERROR] Failed to extract text from {file_path}: {e}")
        text = ""

    return text.strip()