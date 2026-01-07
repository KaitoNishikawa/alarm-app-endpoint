import os
import sys
import json
import boto3
# from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, jsonify, request

current_dir = os.path.dirname(os.path.abspath(__file__))
docker_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, docker_root)

from data_processing.load_data import LoadData
from aws.s3_stuff import S3_Stuff

# load_dotenv()
# access_key = os.getenv('AWS_ACCESS_KEY_ID')
# secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
# 
# if not access_key or not secret_access_key:
#     print("WARNING: AWS Credentials not found in environment variables!")
# else:
#     print("AWS Credentials found.")

s3 = boto3.resource("s3")

app = Flask(__name__)

@app.route('/api/hello')
def hello_world():
    # runner.run_preprocessing(["20251213", "20251214", "20251215", "20251217"])
    return jsonify(message='Hello World (API)')

@app.route('/api/data', methods=["POST"])
def receive():
    if request.is_json:
        json_data = request.get_json()

        data_list = json_data if isinstance(json_data, list) else [json_data]

        for data in data_list:
            accelData, HRData, absolute_start_time, package_start_time, user_id, is_last = LoadData.parse_data_json(data)
            numpy_arrays, absolute_start_time, package_start_time, file_path_endings = LoadData.write_data_to_numpy_array(accelData, HRData, absolute_start_time, package_start_time)
            S3_Stuff.upload_numpy_arrays_to_s3(s3, user_id, absolute_start_time, package_start_time, file_path_endings, numpy_arrays)
            S3_Stuff.upload_is_last_to_s3(s3, user_id, absolute_start_time, is_last)
        
        return jsonify(message="Data received and saved successfully"), 200
    else:
        return jsonify(message="Request was not JSON"), 400
    
@app.route('/api/sleep_data', methods=["POST"])
def receive_sleep_data():
    if request.is_json:
        json_data = request.get_json()
        
        sleep_data_bytes, user_id, session_start_date = LoadData.write_apple_sleep_data_to_json(json_data)
        S3_Stuff.upload_apple_sleep_data_to_s3(s3, user_id, session_start_date, sleep_data_bytes)
        
        return jsonify(message="Sleep data saved successfully"), 200            
    else:
        return jsonify(message="Request was not JSON"), 400
    
@app.route('/api/get_predictions', methods=['POST'])
def get_predictions():
    if request.is_json:
        json_data = request.get_json()

        user_id, session_id = LoadData.parse_prediction_json(json_data)
        
        if not user_id or not session_id:
            return jsonify(error="Missing userID or sessionID"), 400

        prediction_key = f"users/{user_id}/{session_id}/predictions/0721_predictions.json"
        
        try:
            # Check if the file exists in S3
            obj = s3.Object('s3-smart-alarm-app', prediction_key)
            data = obj.get()['Body'].read().decode('utf-8')
            predictions = json.loads(data)
            
            return jsonify(predictions=predictions, status=str(predictions[-10:])), 200
        except s3.meta.client.exceptions.NoSuchKey:
            # File isn't ready yet
            return jsonify(predictions=[], status="no prediction file"), 202 
        except Exception as e:
            return jsonify(status=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)