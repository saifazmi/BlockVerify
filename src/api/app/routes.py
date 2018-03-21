from flask import jsonify, request
from app import app, errors, blockchain
import transaction


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


@app.route('/api/transaction/new', methods=['POST'])
def new_transaction():
    data = request.get_json()
    required = ['file_hash', 'author_key', 'signature']

    if not all(k in data for k in required):
        return errors.bad_request(
            'missing values, must provide file_hash, author_key, signature')

    txn = transaction.Transaction()
    txn.from_dict(data)
    blockchain.transaction_pool.add_transaction(txn)
    respone = {'message': 'Transaction will be added to Block #{}'.format(
        blockchain.current_block.index + 1
    )}
    return jsonify(respone)


@app.route('/api/mine', methods=['GET'])
def mine():
    pass
