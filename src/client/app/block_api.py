import json
import requests

BASE_URL = 'http://localhost:6000/api'


def add_to_chain(file_data):
    endpoint = f'{BASE_URL}/transaction/new'
    data = {
            'file_hash': file_data['file_hash'],
            'author_key': file_data['sign_key'],
            'signature': file_data['file_signature']
    }
    response = requests.post(endpoint, json=data)

    return (response.status_code, json.loads(response.text))


def chain_search_file(filehash):
    endpoint = f'{BASE_URL}/chain/search/file/{filehash}'
    response = requests.get(endpoint)

    return (response.status_code, json.loads(response.text))


if __name__ == '__main__':
    code, res = chain_search_file('1c5c629c09f20a7640c8a789994494067419d70c2e10350829f2f3b69f54d2f6')
    print(code)
    print(res.get('txn').get('signature'))
