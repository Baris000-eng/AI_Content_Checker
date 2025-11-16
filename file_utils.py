import os
from PyPDF2 import PdfReader
import docx
import config
import numpy as np 
from PIL import Image
import io 
from pdf2image import convert_from_bytes
import easyocr
import config



# Initialize the EasyOCR reader once 
ocr_reader = easyocr.Reader(['en', 'tr', 'de', 'fr'])  

def process_image_for_ocr(file):
    """
    Process image files (PNG, JPG, JPEG, GIF, BMP, TIFF) for OCR extraction.
    Returns the extracted text.
    """
    ext = file.filename.rsplit('.', 1)[1].lower()
    text = ""

    try:
        
        # Open the image using Pillow (for PNG, JPG, JPEG, GIF, BMP, TIFF)
        img = Image.open(file)
        
        # Convert the image to an RGB format
        img = img.convert('RGB')

        # Convert the image to a numpy array for EasyOCR
        img_array = np.array(img)

        # Run OCR using EasyOCR
        ocr_result = ocr_reader.readtext(img_array, detail=0)
        if ocr_result:
            text = "\n".join(ocr_result)
        else:
            print("No text detected in the image.")
    
    except Exception as e:
        print(f"Error processing image for OCR: {e}")

    return text


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
    text = ""  # This will store the OCR ext output

    try:
        # Read the file stream into memory
        file_stream = io.BytesIO(file.read())  

        # Reset the original stream
        file_stream.seek(0)   

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
                
                if not text:  # If no text is found in the PDF, fall back to OCR
                    print("No extractable text found, falling back to OCR...")
                    pdf_bytes = file_stream.read()
                    images = convert_from_bytes(pdf_bytes)  # Convert PDF to images
                    print(f"Number of images generated: {len(images)}")

                    # OCR each image in the PDF (OCR-only case)
                    for i, img in enumerate(images):
                        img_array = np.array(img)  # Convert image to array for OCR
                        ocr_result = ocr_reader.readtext(img_array, detail=0)  # Use EasyOCR for OCR
                        print(f"OCR result for page {i+1}: {ocr_result}")

                        if ocr_result:
                            text += "\n".join(ocr_result) + "\n"
                        else:
                            print(f"No text detected on page {i+1}")
                    
                    print(f"\nOCR Text Extracted:\n{text}")
                    
            except Exception as e: 
                print(f"Error reading PDF for text extraction: {e}")

        elif ext in ('jpg', 'jpeg', 'png', 'bmp', 'tiff', 'gif'):
            text = process_image_for_ocr(file)

        
        elif ext in ('docx', 'doc'):
            # Extract text from Word document
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        print(f"[ERROR] Failed to extract text from {filename}: {e}")

    return text.strip()

