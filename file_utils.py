import os
from PyPDF2 import PdfReader
import docx
import config
import numpy as np 
from pdf2image import convert_from_bytes
import easyocr

# Initialize the EasyOCR reader once 
reader = easyocr.Reader(['en', 'tr', 'de', 'fr'])  


def allowed_file(filename):
    """ Check if the uploaded file has a valid extension """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def extract_text(file):
    """
    Extracts text from uploaded file (.pdf, .docx, .txt).
    Uses OCR for scanned PDFs.
    """
    filename = file.filename
    ext = filename.rsplit('.', 1)[1].lower()
    text = ""

    try:
        file.stream.seek(0)
        # ✅ Handle plain text files
        if ext == 'txt':
            text = file.read().decode('utf-8', errors='ignore')
        # ✅ Handle PDFs entirely in memory
        elif ext == 'pdf':
            # Try normal text extraction
            reader = PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            # Fallback to OCR if no text found
            if text.strip() == "" and len(reader.pages) > 0:
                pdf_bytes = file.read()
                images = convert_from_bytes(pdf_bytes)
                for img in images:
                    # Convert PIL image to array for EasyOCR
                    img_array = np.array(img)
                    result = reader.readtext(img_array, detail=0)  
                    text += "\n".join(result) + "\n"

        # ✅ Handle Word documents
        elif ext in ('docx', 'doc'):
            # docx.Document() requires a file-like object, not bytes
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        print(f"[ERROR] Failed to extract text from {filename}: {e}")
        text = ""

    return text.strip()