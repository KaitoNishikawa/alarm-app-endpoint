import os
import sys
import boto3
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
docker_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, docker_root)

from aws.s3_stuff import S3_Stuff

load_dotenv()
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

user_id = '0001'
date = '20241222'

heart_path = 'data/heart_rate/' + date + '_heartrate.txt'
label_path = 'data/labels/' + date + '_labeled_sleep.txt'
motion_path = 'data/motion/' + date + '_acceleration.txt'

paths = [heart_path, label_path, motion_path]

s3 = boto3.resource(
    "s3",
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_access_key,
)

S3_Stuff.upload_files(s3, user_id, date, paths)






