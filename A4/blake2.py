import hashlib
import json
import requests

def lambda_handler(event, context):
    # Extract necessary information from the event
    banner = "B00937694"
    action = "blake2"  # Updated action to indicate BLAKE2b hashing with a 32-byte digest size
    value = event['value']
    arn = "arn:aws:lambda:us-east-1:833413257782:function:Blake2"

    # Perform BLAKE2b hashing with a 32-byte digest size
    hashed_value = hash_blake2b(value, digest_size=32)

    # Prepare the result payload
    result_payload = {
        "banner": banner,
        "result": hashed_value,
        "arn": arn,
        "action": action,
        "value": value
    }

    # Send the result to the specified endpoint (/end)
    send_result_to_app(result_payload, "http://129.173.67.184:6000/end")

    return {
        'statusCode': 200,
        'body': json.dumps('Hashing complete!')
    }

def hash_blake2b(data, digest_size=32):
    # Perform BLAKE2b hashing with the specified digest size using hashlib
    blake2b_hash = hashlib.blake2b(digest_size=digest_size)
    blake2b_hash.update(data.encode('utf-8'))
    return blake2b_hash.hexdigest()

def send_result_to_app(result, app_url):
    # Send a POST request to the provided app_url
    response = requests.post(app_url, json=result)
    
    if response.status_code == 200:
        print("Result sent successfully")
    else:
        print(f"Failed to send result. Status code: {response.status_code}, Response: {response.text}")
