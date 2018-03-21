from flask import jsonify
from app import app


@app.route('/api')
def api():
    response = {
        'api_version': 0.1,
        'methods': {
            'GET': [
                '/api'
            ],
            'POST': []
        }
    }
    return jsonify(response)


@app.route('/chain', methods=['GET'])
def chain():
    pass
