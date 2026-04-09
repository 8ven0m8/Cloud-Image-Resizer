from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from io import BytesIO
import requests

load_dotenv()

app = Flask(__name__)

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# -------------------------------
# SECURITY SCANNER
# -------------------------------
def security_scan(file, file_bytes):
    allowed_formats = ["jpg", "jpeg", "png"]
    max_size = 2 * 1024 * 1024

    filename = file.filename.lower()
    size = len(file_bytes)

    if not any(filename.endswith(ext) for ext in allowed_formats):
        return "Blocked: Invalid file type"

    if size > max_size:
        return "Blocked: File too large"

    if "virus" in filename or "malware" in filename:
        return "Blocked: Suspicious filename"

    if size < 1000:
        return "Blocked: Suspiciously small file"

    return "Safe"


def log_event(message):
    with open("../security_log.txt", "a") as f:
        f.write(message + "\n")


# -------------------------------
# FRONTEND
# -------------------------------
@app.route("/")
def home():
    return send_from_directory("../Frontend", "index.html")


# -------------------------------
# UPLOAD
# -------------------------------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")

    if not file:
        return jsonify({"status": "No file uploaded"})

    width = int(request.form.get("width", 300))
    height = int(request.form.get("height", 300))

    file_bytes = file.read()

    scan_result = security_scan(file, file_bytes)
    log_event(f"{file.filename} -> {scan_result}")

    if scan_result != "Safe":
        return jsonify({"status": scan_result})

    try:
        # Upload original
        cloudinary.uploader.upload(file_bytes, folder="input_image")

        # Upload resized
        resized = cloudinary.uploader.upload(
            file_bytes,
            folder="output_image",
            transformation=[{
                "width": width,
                "height": height,
                "crop": "fill"
            }]
        )

        return jsonify({
            "status": "Safe",
            "url": resized["secure_url"]
        })

    except Exception as e:
        return jsonify({"status": str(e)})


# -------------------------------
# DOWNLOAD (FIXED)
# -------------------------------
@app.route("/download", methods=["GET"])
def download():
    print("DOWNLOAD HIT")

    url = request.args.get("url")
    print("URL:", url)

    if not url:
        return "No URL provided", 400

    try:
        response = requests.get(url)

        if response.status_code != 200:
            return "Failed to fetch image", 500

        return send_file(
            BytesIO(response.content),
            mimetype=response.headers.get("Content-Type", "image/jpeg"),
            as_attachment=True,
            download_name="resized_image.jpg"
        )

    except Exception as e:
        return str(e), 500


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)