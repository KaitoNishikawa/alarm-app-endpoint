import io
import datetime
import numpy as np

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
    
    def upload_numpy_arrays_to_s3(s3, user_id, absolute_start_time, package_start_time, file_path_endings, numpy_arrays):
        bucket_name = 's3-smart-alarm-app'
        for index, npy_array in enumerate(numpy_arrays):
            file_path_ending = file_path_endings[index]
            data_type = file_path_ending[:file_path_ending.index('.')]

            absolute_timestamp = datetime.datetime.fromtimestamp(round(absolute_start_time))
            package_timestamp = datetime.datetime.fromtimestamp(round(package_start_time))

            key = f"users/{user_id}/{absolute_timestamp.strftime('%Y%m%d_%H%M%S')}/{data_type}/{package_timestamp.strftime('%Y%m%d_%H%M%S')}_{file_path_ending}"

            try:
                buffer = io.BytesIO()
                np.save(buffer, npy_array)
                buffer.seek(0)
                s3.meta.client.put_object(Bucket=bucket_name, Key=key, Body=buffer)
                print(f"Uploaded to s3://{bucket_name}/{key} directly from memory.")
            except ClientError as e:
                print(f"Couldn't upload file {data_type} to {bucket_name}.")
                print(f"S3 Error: {e.response['Error']['Message']}")
            except Exception as e:
                print(f"Couldn't upload file {data_type} to {bucket_name}.")
                print(f"Other Error: {e}")

    # def upload_apple_sleep_data_to_s3(s3, user_id, session_start_date, file_path):
    #     timestamp = datetime.datetime.fromtimestamp(round(session_start_date))
    #     bucket = s3.Bucket('s3-smart-alarm-app')

    #     key = f'users/{user_id}/{timestamp.strftime('%Y%m%d_%H%M%S')}/apple_sleep_data/{timestamp.strftime('%Y%m%d_%H%M%S')}_apple_sleep_data.json'
    #     obj = bucket.Object(key)
    #     try:
    #         obj.upload_file(file_path)
    #         print(
    #             f"Uploaded file {file_path} into bucket {bucket.name} with key {obj.key}."
    #         )
    #     except S3UploadFailedError as err:
    #         print(f"Couldn't upload file {file_path} to {bucket.name}.")
    #         print(f"\t{err}")
    
    def upload_apple_sleep_data_to_s3(s3, user_id, session_start_date, sleep_data):
        bucket_name = 's3-smart-alarm-app'
        timestamp = datetime.datetime.fromtimestamp(round(session_start_date))
        key = f"users/{user_id}/{timestamp.strftime('%Y%m%d_%H%M%S')}/apple_sleep_data/{timestamp.strftime('%Y%m%d_%H%M%S')}_apple_sleep_data.json"
        try:
            s3.meta.client.put_object(Bucket=bucket_name, Key=key, Body=sleep_data)
            print(f"Uploaded to s3://{bucket_name}/{key} directly from memory.")
        except ClientError as e:
            print(f"Couldn't upload file sleep data to {bucket_name}.")
            print(f"S3 Error: {e.response['Error']['Message']}")
        except Exception as e:
            print(f"Couldn't upload file sleep data to {bucket_name}.")
            print(f"Other Error: {e}")

