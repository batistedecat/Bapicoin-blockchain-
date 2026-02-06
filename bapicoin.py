import hashlib as hasher
from time import time
import json
from uuid import uuid4
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        #create genesis block
        self.new_block(proof = 100, previous_hash=1)

    def register_node(self, address):
        # method for adding neighbouring nodes to our Network
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def new_block(self, proof, previous_hash = None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_block(self.chain[-1]),
        }
        self.chain.append(block)
        self.current_transactions = []
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        return self.last_block['index'] + 1

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
        return geuss_hash[:2] == '00'

    def valid_chain(self, chain):
        last_block = chain[0] #assumes the genesis block is trusted
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            #which blocks are undergoing the comparison tests
            print(f"{last_block}")
            print(f"{block}")
            print("\n--------------------------\n")
            #is the previous blocks hash correct?
            if block["previous_hash"] != self.hash_block(last_block): #first test
                return False
            #correct PoW
            if not self.valid_proof(last_block["proof"], block["proof"]):
                return False

            #move window forward
            last_block = block
            current_index +=1
        return True

    def resolve_conflicts(self): #consensus algorithm
        #longest chain survives
        buren = self.nodes
        new_chain = None
        #are there chaines longer that ours
        max_length = len(self.chain)

        for node in buren:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200: #200 = OK
                length = response.json()['length'] #length of that node
                chain = response.json()['chain'] #chain of that node
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        else:
            return False


app = Flask(__name__)

#output is 550e8400e29b41d4a716446655440000 or another random Universally Unique Identifier
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

@app.route("/test_connection", methods = ["GET"])
def test_connection():
    return {}, 200
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
        sender = "system",
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

@app.route("/nodes/register", methods = ["POST"])
def register_nodes():
    values = request.get_json()

    nodes = values.get("nodes")
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    for node in nodes:
        bapicoin.register_node(node)

    response = {
        "message": "New nodes have been added",
        "total_nodes": list(bapicoin.nodes)
    }
    return jsonify(response), 201

@app.route("/nodes/resolve", methods = ["GET"])
def concensus():
    replaced = bapicoin.resolve_conflicts()

    if replaced:
        response = {
            "message": "Our chain was replaced",
            "new_chain": bapicoin.chain
        }
    else:
        response = {
            "message": "Our chian is authoritative",
            "chain": bapicoin.chain
        }
    return jsonify(response), 200





# #run server on port 5000
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port = 5001)