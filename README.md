


# BapiCoin — A Minimal Educational Blockchain in Python

BapiCoin is a deliberately simple blockchain implementation written in Python using Flask.  
I build it for educational purposes; not for security, performance, or real-world deployment.

This project exists to make blockchains understandable by stripping them down to their essential moving parts:
hashes, blocks, Proof of Work, transactions, and consensus.

---

## What This Project Demonstrates

- Genesis block creation
- ***SHA-256 cryptographic hashing***
- ***Proof of Work (PoW)***
- Transaction pooling
- Mining rewards
- ***REST-based blockchain interaction***
- Peer node registration
- Chain validation
- Consensus via the longest valid chain

---

## Requirements

- Python 3.7 or newer, i used 3.14
- Flask

Install dependencies:

```bash
pip install flask
````

---

## Running the Blockchain Node

Start the server by running:

```bash
python3 blockchain.py
```

You should see output similar to:

```text
Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)
```

Each node generates a unique identifier (UUID) that is used to receive mining rewards.

---

## Blockchain Data Structure

Each block is a plain Python dictionary serialized to JSON.

A typical block looks like this:

```python
block = {
    'index': 1,
    'timestamp': 123456789.9876543,
    'transactions': [
        {
            'sender': "some hexadecimal string...",
            'recipient': "another hexadecimal string",
            'amount': 100000000
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
```

### Block Fields Explained

* **index** — position of the block in the chain
* **timestamp** — time the block was created
* **transactions** — list of transactions stored in the block
* **proof** — Proof of Work result
* **previous_hash** — cryptographic hash of the previous block

The `previous_hash` field is what links blocks together and makes tampering detectable.

---

## Interacting with the Blockchain from the Terminal

All interaction with the blockchain happens through HTTP requests.
You can use tools like `curl` or Postman. The examples below use `curl` because i do not know how to use Postman yet.

---

## Creating a Transaction

Transactions are sent to the node and placed into a transaction pool.

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "sender": "d4ee26eee15148ee92c6cd394edd974e",
  "recipient": "someone-other-address",
  "amount": 5
}' http://localhost:5001/transactions/new
```

If successful, the node responds with a message indicating which block the transaction will be added to.

Note:
Transactions are **not added to the blockchain immediately**.
They are committed only when a block is mined.

---

## Mining a Block

Mining performs three actions:

1. Runs the Proof of Work algorithm
2. Rewards the miner with newly created coins
3. Writes pending transactions into a new block

To mine a block:

```bash
curl http://localhost:5001/mine
```

The response includes the newly forged block, its proof, and its transactions.

---

## Viewing the Full Blockchain

To inspect the entire blockchain:

```bash
curl http://localhost:5001/chain
```

This returns:

* The full chain
* The total number of blocks

This endpoint is useful for verifying block order, hashes, and Proof of Work.

---

## Node Registration

Multiple nodes can form a small network by registering with each other.

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "nodes": [
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003"
  ]
}' http://localhost:5001/nodes/register
```

---

## Consensus and Conflict Resolution

Consensus is achieved using a simple rule:

> The longest valid chain is considered authoritative.

To trigger conflict resolution:

```bash
curl http://localhost:5001/nodes/resolve
```

If a longer valid chain is found among registered nodes, the local chain is replaced.

---

## Proof of Work Explained

The Proof of Work algorithm searches for a number such that:

```
SHA256(last_proof + proof) starts with "00"
```

This makes block creation computationally expensive while keeping verification fast.

The creation of new "Bapicoin" in the network and mining difficulty can be respectively reduced and increased by simply adding an extra `0`in the `valid_proof` function.

The difficulty is intentionally low to keep the system understandable and mining time short ;)

---

## Known Limitations

This project is **not secure** and **not production-ready**.

It intentionally omits:

* Digital signatures
* Public/private key cryptography
* Transaction validation
* Persistent storage
* Network security
* Advanced fork resolution

These omissions keep the code small and readable.

---

## Educational Purpose

This project is meant to:

* Demystify blockchain internals
* Show how Proof of Work actually functions
* Learn REST-based blockchain interaction
* Provide a foundation for further experimentation

If you can explain Bapicoin without looking at the code, you understand the fundamentals.

---

## Possible Extensions

* Add cryptographic signatures
* Implement wallets
* Persist the blockchain to disk
* Increase Proof of Work difficulty dynamically
* Replace Flask with asynchronous networking
* Add transaction validation rules

Each extension corresponds to a real-world blockchain concept.
