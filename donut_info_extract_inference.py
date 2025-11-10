from pdf2image import convert_from_path
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image

# Load pre-trained Donut model and processor
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")

# Convert PDF to list of images (one for each page)
pdf_path = "path_to_your_document.pdf"
pages = convert_from_path(pdf_path, 300)  # 300 DPI for better quality

# Iterate through each page of the PDF
for page_index, page_image in enumerate(pages):
    print(f"Processing page {page_index + 1}...")

    # Preprocess the page image for the Donut model
    inputs = processor(images=page_image, return_tensors="pt")

    # Perform inference to get the results
    outputs = model.generate(**inputs)

    # Decode the output to get the structured text or content
    result = processor.decode(outputs[0], skip_special_tokens=True)

    # Print the result for the current page
    print(f"Page {page_index + 1} result: {result}")
