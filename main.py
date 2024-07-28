import os
import logging
from flask import Flask, request, jsonify, send_file
from google.cloud import storage

app = Flask(__name__)

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize the Google Cloud Storage client
storage_client = storage.Client()
bucket_name = 'your-gcs-bucket-name'
bucket = storage_client.bucket(bucket_name)

@app.route("/")
def index():
    logging.info("Serving the index.html file.")
    return send_file('src/index.html')

@app.route("/upload", methods=["POST"])
def upload_file():
    logging.info("Received a file upload request.")
    if 'file' not in request.files:
        logging.error("No file part in the request.")
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        logging.error("No selected file.")
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    logging.info(f"Uploading file {filename} to bucket {bucket_name}.")
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    logging.info(f"File {filename} uploaded successfully.")
    return jsonify({"message": f"File {filename} uploaded successfully"}), 200

@app.route("/files", methods=["GET"])
def list_files():
    logging.info("Listing files in the bucket.")
    blobs = bucket.list_blobs()
    files = [{'name': blob.name, 'uploaded_at': blob.time_created.isoformat()} for blob in blobs]
    logging.info(f"Files listed: {files}")
    return jsonify({"files": files}), 200

def main():
    port = int(os.environ.get('PORT', 8080))  # Change port to 8080 for Cloud Run
    logging.info(f"Starting Flask app on port {port}.")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()