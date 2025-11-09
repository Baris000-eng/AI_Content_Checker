from flask import Flask, render_template, request, jsonify
import os
import file_utils
import ai_model
from werkzeug.utils import secure_filename
import config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
@app.route("/predict", methods=["POST"])
def predict():
    text = request.form.get("text", "").strip()
    file = request.files.get("file")

    if file and file_utils.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        text = file_utils.extract_text(filepath)
        os.remove(filepath)  # Optional: remove the uploaded file after extracting text
    elif not text:
        return jsonify({"error": "No text or file provided"}), 400

    # Split text into chunks and predict for each chunk
    chunks = split_into_chunks(text)
    predictions = ai_model.predict_chunks(chunks)

    # Prepare the response with chunks and their probabilities
    result = []
    for i, (ai_prob, human_prob) in enumerate(predictions):
        result.append({
            'chunk': chunks[i],
            'ai_prob': round(ai_prob * 100, 2),  # Convert to percentage
            'human_prob': round(human_prob * 100, 2)  # Convert to percentage
        })

    return jsonify(result)


@app.route("/extract_text", methods=["POST"])
def extract_text_route():
    file = request.files.get("file")
    if not file or not file_utils.allowed_file(file.filename):
        return jsonify({"error": "No valid file uploaded"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    try:
        text = file_utils.extract_text(filepath)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(filepath)

    return jsonify({"text": text})


@app.route("/")
def index():
    return render_template("index.html")
