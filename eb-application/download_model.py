import requests
import os

def init_model():
    base_url = 'https://macs123-deployment.s3.amazonaws.com/personality_model/'
    print(f"Base URL: {base_url}")
    # Define the local directory to save the downloaded files
    local_dir = 'personality_model/'

    # Create the local directory if it doesn't exist
    os.makedirs(local_dir, exist_ok=True)

    # List of files to download (this would normally be retrieved dynamically)
    files_to_download = [
        "config.json",  # Replace with actual file names
        "model.safetensors",
    ]

    # Download each file
    for file_name in files_to_download:
        file_url = f'{base_url}{file_name}'
        local_path = os.path.join(local_dir, file_name)
        
        # Create local directory structure if it doesn't exist    
        # Download the file
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {file_name} to {local_path}")
        else:
            print(f"Failed to download {file_name}: {response.status_code, response.text}")

def init_tokenizer():
    base_url = 'https://macs123-deployment.s3.amazonaws.com/personality_tokenizer/'
    print(f"Base URL: {base_url}")
    # Define the local directory to save the downloaded files
    local_dir = 'personality_tokenizer/'

    # Create the local directory if it doesn't exist
    os.makedirs(local_dir, exist_ok=True)

    # List of files to download (this would normally be retrieved dynamically)
    files_to_download = [
        "special_tokens_map.json",  # Replace with actual file names
        "tokenizer_config.json",
        "tokenizer.json",
        "vocab.txt"
    ]

    # Download each file
    for file_name in files_to_download:
        file_url = f'{base_url}{file_name}'
        local_path = os.path.join(local_dir, file_name)
        
        # Create local directory structure if it doesn't exist    
        # Download the file
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {file_name} to {local_path}")
        else:
            print(f"Failed to download {file_name}: {response.status_code, response.text}")

