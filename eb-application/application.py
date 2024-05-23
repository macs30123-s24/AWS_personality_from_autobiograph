import os
import logging
from flask import Flask, request, jsonify
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import boto3
from download_model import init_model, init_tokenizer

# Initialize the model and tokenizer
init_model()
init_tokenizer()

app = Flask(__name__)
application = app
# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Ensure the /tmp/huggingface directory exists
cache_dir = '/tmp/huggingface'
os.makedirs(cache_dir, exist_ok=True)
# Set the environment variable for Hugging Face Transformers
os.environ['TRANSFORMERS_CACHE'] = cache_dir

# Initialize boto3 clients
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
bucket_name = 'macs123-deployment'

# Ensure nltk resources are downloaded
logging.info("Loaded modules!")

# Load the tokenizer and model
tokenizer_dir = 'personality_tokenizer/'
model_dir = 'personality_model/'

if os.path.exists(tokenizer_dir):
    logging.info("Tokenizer directory exists. Contents:")
    logging.info(os.listdir(tokenizer_dir))
else:
    logging.warning("Tokenizer directory does not exist.")
    # Download tokenizer files from S3 if necessary
    # Uncomment and modify the following lines if needed
    # s3_client.download_file(bucket_name, 'path/to/tokenizer/file', tokenizer_dir + 'file')

logging.info("Loading tokenizer!")
try:
    tokenizer = BertTokenizer.from_pretrained(tokenizer_dir)
    logging.info("Loaded tokenizer!")
except Exception as e:
    logging.error("Error loading tokenizer: %s", str(e))

if os.path.exists(model_dir):
    logging.info("Model directory exists. Contents:")
    logging.info(os.listdir(model_dir))
else:
    logging.warning("Model directory does not exist.")
    # Download model files from S3 if necessary
    # Uncomment and modify the following lines if needed
    # s3_client.download_file(bucket_name, 'path/to/model/file', model_dir + 'file')

logging.info("Loading model...")
try:
    model = BertForSequenceClassification.from_pretrained(model_dir)
    logging.info("Loaded model!")
except Exception as e:
    logging.error("Error loading model: %s", str(e))

# Define the personality detection function
def personality_detection(text):
    try:
        inputs = tokenizer(text, truncation=True, padding=True, return_tensors="pt")
        outputs = model(**inputs)
        predictions = outputs.logits.squeeze().detach().numpy()
        label_names = ['Extroversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']
        result = {label_names[i]: float(predictions[i]) for i in range(len(label_names))}
        return result
    except Exception as e:
        logging.error("Error in personality_detection: %s", str(e))
        return {"error": str(e)}

@app.route('/detect_personality_chunks', methods=['POST'])
def detect_personality():
    try:
        data = request.json
        if 'chunks' not in data:
            return jsonify({'error': 'Invalid input format. Expected "chunks" key.'}), 400

        chunks = data['chunks']
        results = [personality_detection(chunk.replace('\n', ' ')) for chunk in chunks]
        
        return jsonify(results)
    except Exception as e:
        logging.error("Error in /detect_personality endpoint: %s", str(e))
        return jsonify({'error': str(e)}), 500
    
@app.route('/detect_personality', methods=['POST'])
def detect_personality_one_chunk():
    try:
        data = request.json
        if 'chunk' not in data:
            return jsonify({'error': 'Invalid input format. Expected "chunk" key.'}), 400

        chunk = data['chunk']
        result = personality_detection(chunk.replace('\n', ' '))
        
        return jsonify(result)
    except Exception as e:
        logging.error("Error in /detect_personality endpoint: %s", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
