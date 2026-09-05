from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

from security import (
    calculate_sha256,
    analyze_file
)

from database import (
    create_database,
    find_file,
    register_file,
    save_history,
    get_history
)

from ai_analysis import analyze_security
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create upload directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create database
create_database()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_file():
    if "file" not in request.files:
        return jsonify({
            "error": "No file selected"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    filename = secure_filename(file.filename)

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    # Save uploaded file
    file.save(file_path)

    # Calculate SHA-256
    current_hash = calculate_sha256(file_path)

    # Check whether file already exists
    existing_file = find_file(filename)

    # -----------------------------
    # FIRST UPLOAD
    # -----------------------------

    if existing_file is None:
        file_id = register_file(
            filename,
            current_hash
        )

        result = analyze_file(
            current_hash,
            current_hash,
            file_path
        )

        save_history(
            file_id,
            current_hash,
            result["status"],
            result["risk"],
            result["difference"],
            result["execution_time"]
        )

        return jsonify({
            "filename": filename,
            "original_hash": current_hash,
            "current_hash": current_hash,
            "status": "NEW FILE",
            "different_bits": 0,
            "difference": 0,
            "risk": "LOW",
            "execution_time": result["execution_time"]
        })

    # -----------------------------
    # EXISTING FILE
    # -----------------------------

    file_id = existing_file[0]
    original_hash = existing_file[1]

    # Analyze file
    result = analyze_file(
        original_hash,
        current_hash,
        file_path
    )
    result["filename"] = filename
    ai_result = analyze_security(result)

    # Save history
    save_history(
        file_id,
        current_hash,
        result["status"],
        result["risk"],
        result["difference"],
        result["execution_time"]
    )

    return jsonify({
        "filename": filename,
        "original_hash": original_hash,
        "current_hash": current_hash,
        "status": result["status"],
        "different_bits": result["different_bits"],
        "difference": result["difference"],
        "risk": result["risk"],
        "execution_time": result["execution_time"],
        "ai_analysis": ai_result

    })

@app.route("/history")
def history():
    records = get_history()
    history_data = []

    for record in records:
        history_data.append({
            "filename": record[0],
            "hash": record[1],
            "status": record[2],
            "risk": record[3],
            "difference": record[4],
            "execution_time": record[5],
            "checked_at": record[6]
        })
    return jsonify(history_data)

if __name__ == "__main__":
    app.run(debug=True)