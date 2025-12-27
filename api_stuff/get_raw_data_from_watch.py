import os
import sys
import boto3
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, jsonify, request

current_dir = os.path.dirname(os.path.abspath(__file__))
docker_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, docker_root)

from data_processing.load_data import LoadData
from aws.s3_stuff import S3_Stuff

load_dotenv()
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.resource(
    "s3",
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_access_key,
)

file_number = datetime.now().strftime("%Y%m%d")
# file_number = "20241222"
print(f"date: {file_number}")
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    # runner.run_preprocessing(["20251213", "20251214", "20251215", "20251217"])
    return jsonify(message='Hello World')

@app.route('/data', methods=["POST"])
def receive():
    if request.is_json:
        json_data = request.get_json()

        accelData, HRData, absolute_start_time, package_start_time, userID = LoadData.parse_data_json(json_data)
        file_paths, absolute_start_time, package_start_time, file_path_endings = LoadData.write_data_to_files(accelData, HRData, absolute_start_time, package_start_time, docker_root)
        S3_Stuff.upload_motion_files_to_s3(s3, userID, absolute_start_time, package_start_time, file_path_endings, file_paths)
        
        return jsonify(message="Data received and saved successfully"), 200
    else:
        return jsonify(message="Request was not JSON"), 400
    
@app.route('/sleep_data', methods=["POST"])
def receive_sleep_data():
    if request.is_json:
        json_data = request.get_json()
        
        userID, session_start_date, file_path = LoadData.write_apple_sleep_data_to_file(json_data, docker_root)            
        S3_Stuff.upload_apple_sleep_data_to_s3(s3, userID, session_start_date, file_path)
        
        return jsonify(message="Sleep data saved successfully"), 200            
    else:
        return jsonify(message="Request was not JSON"), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)