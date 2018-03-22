import json
import requests

BASE_URL = 'http://localhost:6000/api'


def add_to_chain(file_data):
    endpoint = '/transaction/new'
    data = {
            'file_hash': file_data['file_hash'],
            'author_key': file_data['sign_key'],
            'signature': file_data['file_signature']
    }
    response = requests.post(BASE_URL + endpoint, json=data)

    return (response.status_code, json.loads(response.text))
