
MINING_SENDER = "THE BLOCKCHAIN"
MINING_REWARD = 1
MINING_DIFFICULTY = 2


class Blockchain:

    def __init__(self):
        pass
    def register_node(self, node_url):
        pass
    def submit_transaction(self, sender_address, recipient_address, value, signature):
        pass
    def create_block(self, nonce, previous_hash):
        pass
    def hash(self, block):
        pass
    def proof_of_work(self):
        pass
    def valid_proof(self, transactions, last_hash, nonce, difficulty=MINING_DIFFICULTY):
        pass
    def valid_chain(self, chain):
        pass
    def resolve_conflicts(self):
        pass


