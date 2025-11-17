from flask import Flask, render_template, request, jsonify
import os
import file_utils
import ai_model
import validators
from flask_cors import CORS
import os
from check_url_content import scrape_content
from scrapper import scrap_text
os.environ["TOKENIZERS_PARALLELISM"] = "true"

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

@app.route("/extract-text-from-file-or-plain-text", methods=["POST"])
def extract_text_from_file_or_plain_text():
    text = request.form.get("text", "").strip()
    file = request.files.get("file")

    if file and file_utils.allowed_file(file.filename):
        filename = file.filename 

        # Extract text directly from the in-memory file
        text = file_utils.extract_text(file)

        return jsonify({
            "text": text,
            "filename": filename
        })

    elif not text:
        return jsonify({"error": "No text or file provided"}), 400

    # Only text provided
    text = text.strip()

    return jsonify({"text": text, "filename": None})


@app.route("/predict", methods=["POST"])
def predict():
    text = request.form.get("text", "").strip()
    file = request.files.get("file")

    # Check if the pasted content is a valid URL. If so, parse the URL content. 
    if validators.url(text):
        text = scrap_text(text)

    if not text and not file:
        return jsonify({"error": "No text or file provided"}), 400

    # Extract text from file if uploaded
    if file and file_utils.allowed_file(file.filename):
        text = file_utils.extract_text(file)

    text = text.strip()

    # Split text into chunks
    chunks = split_into_chunks(text)

    # Predict AI/human probabilities for all chunks at once
    predictions = ai_model.predict_chunks(chunks)

    # Prepare JSON response
    results = []
    for chunk, (ai_prob, human_prob) in zip(chunks, predictions):
        results.append({
            "chunk": chunk,
            "ai_prob": ai_prob,
            "human_prob": human_prob
        })

    return jsonify(results)


@app.route("/")
def index():
    return render_template("index.html")
