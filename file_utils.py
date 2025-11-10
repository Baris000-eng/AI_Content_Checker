import os
from PyPDF2 import PdfReader
import docx
import config
import numpy as np 
from pdf2image import convert_from_bytes
import easyocr

# Initialize the EasyOCR reader once 
ocr_reader = easyocr.Reader(['en', 'tr', 'de', 'fr'])  


def allowed_file(filename):
    """ Check if the uploaded file has a valid extension """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def extract_text(file):
    """
    Extracts text from uploaded file (.pdf, .docx, .txt).
    Uses OCR for scanned PDFs or PDFs that fail to extract text.
    """
    filename = file.filename
    ext = filename.rsplit('.', 1)[1].lower()
    text = ""

    try:
        file.stream.seek(0)

        if ext == 'txt':
            text = file.read().decode('utf-8', errors='ignore')

        elif ext == 'pdf':
            try:
                reader = PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            except Exception as e:
                # If PdfReader fails entirely to extract text from PDF, treat the document 
                # as a scanned PDF.
                print(f"[INFO] PdfReader failed, assuming scanned PDF: {e}")
                file.stream.seek(0)
                pdf_bytes = file.read()
                images = convert_from_bytes(pdf_bytes)
                for img in images:
                    img_array = np.array(img)
                    result = ocr_reader.readtext(img_array, detail=0)
                    text += "\n".join(result) + "\n"

        elif ext in ('docx', 'doc'):
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        print(f"[ERROR] Failed to extract text from {filename}: {e}")
        text = ""

    return text.strip()