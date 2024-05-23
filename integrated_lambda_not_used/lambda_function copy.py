''' This function takes in a list of strings and returns a list of dictionaries'''

print("Loading modules...")
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np
import boto3
import os
# Ensure nltk resources are downloaded
print("Loaded modules!")
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
bucket_name = 'macs123-deployment'
prefix = 'personality_tokenizer/'

# Specify the local directory to save the downloaded files
local_dir = '/tmp/personality_tokenizer/'

# Create the local directory if it doesn't exist
os.makedirs(local_dir, exist_ok=True)
bucket_resource = s3_resource.Bucket(bucket_name)
objects_under_prefix = bucket_resource.objects.filter(Prefix=prefix)
tokenizer_dir = '/tmp/personality_tokenizer/'

# Load the tokenizer from the downloaded files
tokenizer = BertTokenizer.from_pretrained(tokenizer_dir)
print("Loaded tokenizer!")
s3_resource = boto3.resource('s3')
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

model = BertForSequenceClassification.from_pretrained(local_dir)
print("Loaded model!")
# Iterate over the objects and print their keys
for obj in objects_under_prefix:
    key = obj.key
    filename = os.path.join(local_dir, os.path.basename(key))
    s3_client.download_file(bucket_name, key, filename)
    print(f"Downloaded {key} to {filename}")

# Define the personality detection function
def personality_detection(text):
    #tokenizer = BertTokenizer.from_pretrained("Minej/bert-base-personality")
    model = BertForSequenceClassification.from_pretrained("Minej/bert-base-personality")
    inputs = tokenizer(text, truncation=True, padding=True, return_tensors="pt")
    outputs = model(**inputs)
    predictions = outputs.logits.squeeze().detach().numpy()
    label_names = ['Extroversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']
    result = {label_names[i]: predictions[i] for i in range(len(label_names))}
    return result


def lambda_handler(event, context):
    results = []
    for chunk in event['chunks']:
        text = chunk.replace('\n', ' ')
        results.append(personality_detection(text))
    return results

'''
{
  "chunks": ["test1" , "test2"]
}
'''  
if __name__ == '__main__':
    event = {
        "chunks": ["test1", "test2"]
    }
    results = lambda_handler(event, None)
    print(results)
    print("Done!") 