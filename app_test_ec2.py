import requests
ec2 = "ec2-35-153-52-203.compute-1.amazonaws.com"
url_chunks = "http://{}:5000/detect_personality_chunks"

url_chunk = "http://{}:5000/detect_personality"

# Example data to send in the POST request
print("Sending request to /detect_personality_chunks")
data = {
    "chunks": [
        "I am very excited to learn about machine learning and artificial intelligence.",
        "Sometimes, I feel a bit anxious about the future and the challenges it holds."
    ]
}

# Sending POST request
response = requests.post(url_chunks.format(ec2), json=data)

# Print the response from the server
print(response.status_code)
print(response.json())


## Parallelizable data
print("Sending request to /detect_personality")
data = {
    "chunk":"Sometimes, I feel a bit anxious about the future and the challenges it holds."
}
# Sending POST request
response = requests.post(url_chunk.format(ec2), json=data)

# Print the response from the server
print(response.status_code)
print(response.json())