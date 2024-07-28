import os
from flask import Flask, request, jsonify, send_file
from google.cloud import storage

app = Flask(__name__)

# Initialize the Google Cloud Storage client
storage_client = storage.Client()
bucket_name = 'gcs_bigmachine_demo/specs'
bucket = storage_client.bucket(bucket_name)

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    return jsonify({"message": f"File {filename} uploaded successfully"}), 200

@app.route("/files", methods=["GET"])
def list_files():
    blobs = bucket.list_blobs()
    files = [blob.name for blob in blobs]
    return jsonify({"files": files}), 200

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()