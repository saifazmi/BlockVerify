from flask import jsonify
from app import app, blockchain


@app.route('/api')
def api():
    response = {
        'api_version': 0.1,
        'methods': {
            'GET': [
                '/api',
                '/api/chain',
                '/api/chain/blocks',
                '/api/chain/blocks/transactions'
            ],
            'POST': []
        }
    }
    return jsonify(response)


@app.route('/api/chain', methods=['GET'])
def chain():
    response = blockchain.to_dict()
    return jsonify(response)


@app.route('/api/chain/blocks', methods=['GET'])
def chain_blocks():
    response = blockchain.to_dict(blocks=True)
    return jsonify(response)


@app.route('/api/chain/blocks/transactions', methods=['GET'])
def chain_blocks_txns():
    response = blockchain.to_dict(blocks=True, txns=True)
    return jsonify(response)
