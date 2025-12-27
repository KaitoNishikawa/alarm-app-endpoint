import os
import boto3
import datetime

from boto3.s3.transfer import S3UploadFailedError
from botocore.exceptions import ClientError

class S3_Stuff():
    def upload_motion_files_to_s3(s3, user_id, absolute_start_time, package_start_time, file_path_endings, file_paths):
        bucket = s3.Bucket('s3-smart-alarm-app')
        for index, file_path in enumerate(file_paths):
            file_path_ending = file_path_endings[index]
            data_type = file_path_ending[:file_path_ending.index('.')]

            absolute_timestamp = datetime.datetime.fromtimestamp(round(absolute_start_time))
            package_timestamp = datetime.datetime.fromtimestamp(round(package_start_time))

            key = f'users/{user_id}/{absolute_timestamp.strftime('%Y%m%d_%H%M%S')}/{data_type}/{package_timestamp.strftime('%Y%m%d_%H%M%S')}_{file_path_ending}'
            obj = bucket.Object(key)
            try:
                obj.upload_file(file_path)
                print(
                    f"Uploaded file {file_path} into bucket {bucket.name} with key {obj.key}."
                )
            except S3UploadFailedError as err:
                print(f"Couldn't upload file {file_path} to {bucket.name}.")
                print(f"\t{err}")

    def upload_apple_sleep_data_to_s3(s3, user_id, session_start_date, file_path):
        timestamp = datetime.datetime.fromtimestamp(round(session_start_date))
        bucket = s3.Bucket('s3-smart-alarm-app')

        key = f'users/{user_id}/{timestamp.strftime('%Y%m%d_%H%M%S')}/apple_sleep_data/{timestamp.strftime('%Y%m%d_%H%M%S')}_apple_sleep_data.json'
        obj = bucket.Object(key)
        try:
            obj.upload_file(file_path)
            print(
                f"Uploaded file {file_path} into bucket {bucket.name} with key {obj.key}."
            )
        except S3UploadFailedError as err:
            print(f"Couldn't upload file {file_path} to {bucket.name}.")
            print(f"\t{err}")

    def upload_files_to_s3_test(s3, user_id, file_number, file_paths):
        bucket = s3.Bucket('s3-smart-alarm-app')
        for file_path in file_paths:
                data_type = file_path.split('/')[1]
                key = f'users/{user_id}/{data_type}/{file_number}_{data_type}.txt'
                obj = bucket.Object(key)
                try:
                    obj.upload_file(file_path)
                    print(
                        f"Uploaded file {file_path} into bucket {bucket.name} with key {obj.key}."
                    )
                except S3UploadFailedError as err:
                    print(f"Couldn't upload file {file_path} to {bucket.name}.")
                    print(f"\t{err}")
