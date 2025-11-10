from flask import Flask, render_template, request, jsonify
import os
import file_utils
import ai_model
from werkzeug.utils import secure_filename
import config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def split_into_chunks(text, chunk_size=300):
    """ Split text into smaller chunks (default size is 300 characters) """
    # You can modify this function to split by sentences or paragraphs
    chunks = []
    while len(text) > chunk_size:
        chunk = text[:chunk_size]
        chunks.append(chunk)
        text = text[chunk_size:]
    if text:
        chunks.append(text)
    return chunks

@app.route("/extract-text", methods=["POST"])
def extract_text():
    text = request.form.get("text", "").strip()
    file = request.files.get("file")

    if file and file_utils.allowed_file(file.filename):
        # Keep original filename (user's file name)
        filename = secure_filename(file.filename)

        # Extract text directly from the in-memory file
        text = file_utils.extract_text(file)

        # You can't really get the user's full system path due to browser security
        # So you can return just the filename
        return jsonify({
            "text": text,
            "filename": filename
        })

    elif not text:
        return jsonify({"error": "No text or file provided"}), 400

    # Only text provided
    return jsonify({"text": text, "filename": None})



@app.route("/")
def index():
    return render_template("index.html")
