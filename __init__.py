# SERVER CODE
# https://fastink.alwaysdata.net/


from flask import Flask, request, jsonify
import boto3
from botocore.client import Config

app = Flask(__name__)

# Cloudflare R2 credentials and configuration
ACCOUNT_ID = "d9be2e86fbfb719e8d476eed3d547f7f"
BUCKET_NAME = "upload"
CLIENT_ACCESS_KEY = "f8c6be874195f94a046f89c82aa8e8fb"
CLIENT_SECRET = "4aca0829b41d9acd35484b4d7e6562cc58f1dd216c8863c44edd3505c0a1c624"
CONNECTION_URL = "https://d9be2e86fbfb719e8d476eed3d547f7f.r2.cloudflarestorage.com"

# Create a client to connect to Cloudflare's R2 Storage
s3_client = boto3.client(
    's3',
    endpoint_url=CONNECTION_URL,
    aws_access_key_id=CLIENT_ACCESS_KEY,
    aws_secret_access_key=CLIENT_SECRET,
    config=Config(signature_version='s3v4'),
    region_name='auto'
)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_key = file.filename

    # Check if the file already exists in the bucket
    try:
        s3_client.head_object(Bucket=BUCKET_NAME, Key=file_key)
        return jsonify({"error": "File already exists"}), 409
    except s3_client.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            pass  # File does not exist, proceed with upload
        else:
            # Log the detailed error response for debugging
            return jsonify({"error": f"Error checking file existence: {error_code}", "details": str(e)}), 500

    # Upload the file to Cloudflare R2
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Body=file.stream  # Stream the file content directly
        )
        return jsonify({"message": "File uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
