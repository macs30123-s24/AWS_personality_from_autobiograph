import boto3
import os
import configparser

# aws_access_key_id = 'ASIASXKQNCIV5ROUGN7Y'
# aws_secret_access_key = '7JO5Zu/plWecSE4p7kLEfIijlqJXgoYN7WV0bUBl'
# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_session_token=aws_session_token  # Optional
# )

# s3_resource = boto3.resource(
#     's3',
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_session_token=aws_session_token  # Optional
# )
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

print("Loaded credentials!")

# Download personality tokenizer files
bucket_name = 'macs123-deployment'
prefix = 'personality_tokenizer/'
local_dir = '/tmp/personality_tokenizer/'
os.makedirs(local_dir, exist_ok=True)
bucket_resource = s3_resource.Bucket(bucket_name)
objects_under_prefix = bucket_resource.objects.filter(Prefix=prefix)
for obj in objects_under_prefix:
    key = obj.key
    filename = os.path.join(local_dir, os.path.basename(key))
    s3_client.download_file(bucket_name, key, filename)
    print(f"Downloaded {key} to {filename}")
print("Loading tokenizer!")

# Download personality model files
bucket_name = 'macs123-deployment'
prefix = 'personality_model/'
local_dir = '/tmp/personality_model/'
os.makedirs(local_dir, exist_ok=True)
bucket_resource = s3_resource.Bucket(bucket_name)
objects_under_prefix = bucket_resource.objects.filter(Prefix=prefix)
for obj in objects_under_prefix:
    key = obj.key
    filename = os.path.join(local_dir, os.path.basename(key))
    s3_client.download_file(bucket_name, key, filename)
    print(f"Downloaded {key} to {filename}")