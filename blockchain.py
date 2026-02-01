import hashlib as hasher
from time import time
import json
from uuid import uuid4
from flask import Flask, jsonify, request

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #create genesis block
        self.new_block(proof = 100, previous_hash=1)

    def new_block(self, proof, previous_hash = None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_block(self.chain[-1]),
        }
        self.current_transactions[:] = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        return self.last_block['index'] +1

    @staticmethod
    def hash_block(block):
        block_string = json.dumps(block, sort_keys=True).encode("utf-8")
        return hasher.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) == False:
            proof +=1
        return proof


    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        geuss_hash = hasher.sha256(guess).hexdigest()
        return geuss_hash[1] == '0'


app = Flask(__name__)

#output is 550e8400e29b41d4a716446655440000 or another Universally Unique Identifier
node_indentifier = str(uuid4()).replace("-", "")
#create an instance of the blockchain
bapicoin = Blockchain()

@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": bapicoin.chain,
        "length": len(bapicoin.chain)
    }
    return jsonify(response), 200

#transaction endpoint
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return "Missing values", 400

    index = bapicoin.new_transaction(values["sender"], values["recipient"], values["amount"])
    response = {"message": f"Transaction will be added to Block number {index}"}
    return jsonify(response), 201

#the Mining endpoint
##calculate the Proof of Work
##reward the miner by adding a transaction granting (us) 3 coin
#Forge the new Block by adding it to the chain

@app.route("/mine", methods = ["GET"])
def mine():
    last_block = bapicoin.last_block
    last_proof = last_block['proof']
    proof = bapicoin.proof_of_work(last_proof)
    bapicoin.new_transaction(
        sender = "0",
        recipient = node_indentifier,
        amount = 3
    )

    previous_hash = bapicoin.hash_block(last_block)
    block = bapicoin.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

#run server on port 5000
if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)