import os
from PyPDF2 import PdfReader
import docx
import config
import numpy as np 
import io 
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
        file_stream = io.BytesIO(file.read())  # Read the file stream into memory
        file_stream.seek(0)  # Reset the original stream (needed for further reading)

        if ext == 'txt':
            text = file.read().decode('utf-8', errors='ignore')

        elif ext == 'pdf':
            # Try to extract text using PyPDF2 for PDF files
            try:
                reader = PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                if not text: 
                    pdf_bytes = file_stream.read()
                    images = convert_from_bytes(pdf_bytes)  # Convert PDF to images
                    print(f"Number of images generated: {len(images)}")

                    # OCR each image in the PDF
                    for i, img in enumerate(images):
                        img_array = np.array(img)  # Convert image to array for OCR
                        ocr_result = ocr_reader.readtext(img_array, detail=0)  # Use EasyOCR for OCR
                        print(f"[INFO] OCR result for page {i+1}: {ocr_result}")

                        if ocr_result:
                            text += "\n".join(ocr_result) + "\n"
                        else:
                            print(f"[INFO] No text detected on page {i+1}")
                    
            except Exception as e: 
                print(e) 

        elif ext in ('docx', 'doc'):
            # Extract text from Word document
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        print(f"[ERROR] Failed to extract text from {filename}: {e}")

    return text.strip()