import os

# Flask upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

# Model settings
MODEL_NAME = "roberta-base-openai-detector"  # Replace with actual Hugging Face model if different
