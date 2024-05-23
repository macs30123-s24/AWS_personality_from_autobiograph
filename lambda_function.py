''' Lambda Function that uses the EC2 Backend Service '''

import json
import requests

def lambda_handler(event, context):
    base_url = "http://ec2-35-153-52-203.compute-1.amazonaws.com:5000"

    try:
        # Parse the incoming event as JSON
        data = event
        # Determine which endpoint to call based on the presence of 'chunks' or 'chunk' in the data
        if 'chunks' in data:
            url = f"{base_url}/detect_personality_chunks"
            payload = {
                "chunks": data['chunks']
            }
        elif 'chunk' in data:
            url = f"{base_url}/detect_personality"
            payload = {
                "chunk": data['chunk']
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid input format. Expected "chunks" or "chunk" key.'})
            }
        
        # Make the POST request to the determined URL
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Return the response from the API
        return {
            'statusCode': response.status_code,
            'body': json.dumps(response.json())
        }

    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format in request body.'})
        }

    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input format. Expected "body" key in event.'})
        }
