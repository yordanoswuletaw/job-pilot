import requests
import os
from dotenv import load_dotenv
from payloads import define_payloads
from response_formatter import format_response

load_dotenv()

def find_jobs():
    url = os.getenv('SERPER_URL')
    payloads = define_payloads()
    headers = {
        'X-API-KEY': os.getenv('SERPER_API_KEY'),
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payloads)
    jobs = format_response(response.json())
    return jobs

if __name__ == "__main__":
    find_jobs()