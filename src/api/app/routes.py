from flask import jsonify, request
from app import app, db, errors, blockchain
from app.models import File


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
                '/api/chain/search/file/<file_hash>',
                '/api/mine',
                '/api/blocks',
                '/api/blocks/<int:index>',
                '/api/blocks/<block_hash>'
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


@app.route('/api/chain/search/file/<file_hash>', methods=['GET'])
def chain_file_search(file_hash):
    response = {
        'search_for': file_hash,
        'file_found': False
    }

    file = File.query.filter_by(file_hash=file_hash).first()
    if file is None:
        return errors.error_response(404, 'file not found')
    else:
        response['file_found'] = True
        response['message'] = 'file found'
        txn = blockchain.blocks[file.block_index].transactions[file.txn_index]
        response['txn'] = txn.to_dict()
        response['timestamp'] = blockchain.blocks[file.block_index].timestamp
        return jsonify(response), 200


# MINE ROUTES
@app.route('/api/mine', methods=['GET'])
def mine():
    if len(blockchain.transaction_pool) == 0:
        return errors.bad_request('transaction pool is empty')

    block_index = blockchain.mine()
    txn_index = 0
    for txn in blockchain.blocks[block_index].transactions:
        file = File(
            file_hash=txn.file_hash,
            block_hash=blockchain.blocks[block_index].block_hash,
            block_index=block_index,
            txn_index=txn_index)
        db.session.add(file)
        txn_index += 1
    db.session.commit()

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

    # check if txn already exists in blockchain
    file = File.query.filter_by(file_hash=data['file_hash']).first()
    if file is not None:
        return errors.error_response(403, 'file already exists')

    # check if txn already exists in txn pool
    for txn in blockchain.transaction_pool:
        if data['file_hash'] == txn.file_hash:
            return errors.error_response(
                403, 'file in transaction pool, wait for block to be mined')

    blockchain.add_transaction(data)
    respone = {'message': 'Transaction will be added to Block #{}'.format(
        blockchain.current_block.index + 1
    )}
    return jsonify(respone), 201
