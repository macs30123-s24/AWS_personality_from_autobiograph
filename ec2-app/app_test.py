import requests

url = "http://127.0.0.1:5000/detect_personality"

# Example data to send in the POST request
data = {
    "chunks": [
        "I am very excited to learn about machine learning and artificial intelligence.",
        "Sometimes, I feel a bit anxious about the future and the challenges it holds."
    ]
}

# Sending POST request
response = requests.post(url, json=data)

# Print the response from the server
print(response.status_code)
print(response.json())