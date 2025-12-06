# app.py
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__, static_folder='.', static_url_path='/')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Simple health
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat() + "Z"})

# Main endpoint that accepts form-data (question, language, voice) and files
@app.route("/api/legal", methods=["POST"])
def legal():
    try:
        # text fields
        question = request.form.get("question", "")
        language = request.form.get("language", "en")
        voice = request.form.get("voice", "off")

        saved_files = []
        # handle multiple files with field name 'files'
        if "files" in request.files:
            files = request.files.getlist("files")
        else:
            files = []

        for f in files:
            # sanitize filename lightly
            filename = f.filename
            # prefix with timestamp to avoid collision
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
            safe_name = f"{timestamp}_{filename}"
            path = os.path.join(UPLOAD_DIR, safe_name)
            f.save(path)
            saved_files.append(safe_name)

        # ------- Mock AI logic here -------
        # For a real AI integration use OpenAI or other model (see commented example below)
        # Keep the reply simple and user-friendly — explain rights and next steps
        # DO NOT give actual legal advice; this is for demonstration.

        # Build a helpful response
        steps = [
            "1) Collect documents (land papers, ID, any receipts, photos).",
            "2) Try local resolution: speak with the Panchayat / village elder.",
            "3) If not resolved, register a written complaint at the local police station (FIR) or consult a legal aid organisation.",
            "4) Keep copies of all documents and evidence (photos, witnesses' names).",
            "5) If you want, submit the documents to a lawyer or legal aid — we can connect you."
        ]
        files_txt = ("No files uploaded." if not saved_files else
                     f"Saved files: {', '.join(saved_files)}")

        answer = (f"Language: {language}\n\nYou asked: {question}\n\n"
                  f"{files_txt}\n\n"
                  "Suggested next steps:\n" + "\n".join(steps))

        # Return JSON
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: serve index.html if someone opens root
@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
