from flask import jsonify, request
from app import app, errors, blockchain


@app.route('/api')
def api():
    response = {
        'api_version': 0.1,
        'methods': {
            'GET': [
                '/api',
                '/api/chain',
                '/api/chain/blocks',
                '/api/chain/blocks/transactions',
                '/api/chain/validate',
                '/api/mine'
            ],
            'POST': [
                '/api/transaction/new'
            ]
        }
    }
    return jsonify(response)


# CHAIN ROUTES
@app.route('/api/chain', methods=['GET'])
def chain():
    response = blockchain.to_dict()
    return jsonify(response), 200


@app.route('/api/chain/blocks', methods=['GET'])
def chain_blocks():
    response = blockchain.to_dict(blocks=True)
    return jsonify(response), 200


@app.route('/api/chain/blocks/transactions', methods=['GET'])
def chain_blocks_txns():
    response = blockchain.to_dict(blocks=True, txns=True)
    return jsonify(response), 200


@app.route('/api/chain/validate', methods=['GET'])
def chain_validate():
    is_valid = blockchain.verify_chain()
    respone = {
        'is_valid': is_valid
    }
    if is_valid:
        respone['message'] = 'chain passed validation.'
    else:
        respone['message'] = 'chain failed validation.'
    return jsonify(respone), 200


@app.route('/api/chain/search/file/<file_hash>')
def chain_file_search(file_hash):
    response = {
        'search_for': file_hash,
        'file_found': False
    }

    for block in blockchain.blocks:
        for txn in block.transactions:
            if txn.file_hash == file_hash:
                response['file_found'] = True
                response['message'] = 'file found'
                response['txn'] = txn.to_dict()

    if response['file_found']:
        return jsonify(response), 200
    else:
        return errors.error_response(404, 'file not found')


# MINE ROUTES
@app.route('/api/mine', methods=['GET'])
def mine():
    if len(blockchain.transaction_pool) == 0:
        return errors.bad_request('transaction pool is empty')

    block_index = blockchain.mine()
    response = {
        'message': 'new block created',
        'block': blockchain.blocks[block_index].to_dict(txns=False)
    }
    return jsonify(response), 201


# BLOCKS ROUTES
@app.route('/api/blocks', methods=['GET'])
def blocks():
    response = {
        'blocks': [block.to_dict(txns=False) for block in blockchain.blocks]
    }
    return jsonify(response), 200


@app.route('/api/blocks/<int:index>', methods=['GET'])
def block_by_index(index):
    if index > len(blockchain.blocks) - 1:
        return errors.error_response(404, 'block not found')
    return jsonify(blockchain.blocks[index].to_dict(txns=True)), 200


@app.route('/api/blocks/<block_hash>', methods=['GET'])
def block_by_hash(block_hash):
    block = None
    for b in blockchain.blocks:
        if b.block_hash == block_hash:
            block = b
    if block is None:
        return errors.error_response(404, 'block not found')

    return jsonify(blockchain.blocks[block.index].to_dict(txns=True)), 200


# TRANSACTION ROUTES
@app.route('/api/transaction/new', methods=['POST'])
def new_transaction():
    data = request.get_json()

     # 400: bad request check
    if data is None:
        return errors.bad_request('expected json data in body')
    required = ['file_hash', 'author_key', 'signature']
    if not all(k in data for k in required):
        return errors.bad_request(
            'missing values, must provide file_hash, author_key, signature')

    # check if tranx already exists in
    if blockchain.file_exists(data['file_hash']):
        return errors.error_response(403, 'file already exists')

    blockchain.add_transaction(data)
    respone = {'message': 'Transaction will be added to Block #{}'.format(
        blockchain.current_block.index + 1
    )}
    return jsonify(respone), 201
