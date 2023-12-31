# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 16:11:35 2023

@author: franc
"""

# install:
# Flask==0.12.0: pip install Flask==1.1.2
# Client HTTP Postman

# Import libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify


# 1 - Create blockchain 
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_bloc(proof = 1, previous_hash = '0')
    
    def create_bloc(self, proof, previous_hash):
        block = {
            'index'        : len(self.chain)+1,
            'timestamp'    : str(datetime.datetime.now()),
            'proof'        : proof,
            'previous_hash': previous_hash
            }
        self.chain.append(block)
        return block
    
    def get_previous_bloc(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof= False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash2(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash2(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True



# 2 - mining a chain block

# Create aplication web
app = Flask(__name__)

# Create Blockchain
blockchain = Blockchain()

# Mining
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_bloc()
    previous_proof = previous_block['proof']
    proof          = blockchain.proof_of_work(previous_proof)
    previous_hash  = blockchain.hash2(previous_block)
    block          = blockchain.create_bloc(proof, previous_hash)
    response = {
        'message'       : '¡Congratulations!, you have mined a block!',
        'index'         : block['index'],
        'timestamp'     : block['timestamp'],
        'proof'         : block['proof'],
        'previous_hash' : block['previous_hash']
        }
    return jsonify(response), 200

# Get chain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {
        'chain'  : blockchain.chain,
        'length' : len(blockchain.chain)
        }
    return jsonify(response), 200

# Run the app
app.run(host='127.0.0.1', port='5000')