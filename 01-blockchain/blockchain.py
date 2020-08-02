import json
import requests

from block import Block
from transaction import Transaction
from utility.hash_util import hash_block
from utility.verification import Verification
from wallet import Wallet

# Number of coins rewarded for each mining
MINING_REWARD = 10


class Blockchain:
    """ Represents the underlying blockchain.

    Attributes:
        chain (:obj:`list` of `Block`): A list of `Block`s chained together to form
            the blockchain.
        __open_transactions (:obj:`list` of `Transaction`): A list of open `Transaction`s.
        public_key (`str`): The public key assigined to the `wallet` of the node
            owning this blockchain.
        __peer_nodes (:obj:`set` of `str`): :obj:`set` of `node URL`s of `Node`s that
            is connecting to the node owning this blockchain.
        node_id (`int`): The id of the node hosting the app
            (equal to the `port` argument passed in when starting the app).
        resolve_conflicts (`bool`): False meams there is no need to resolve blockchain
            conflicts. True means vice versa.
    """

    def __init__(self, public_key, node_id):
        # Genesis block
        # Note that, for the genesis block, proof can be initialized with any value
        genesis_block = Block(index=0, previous_hash='',
                              transactions=[], proof=100, timestamp=0)
        # Initialize a blockchain as a list
        self.chain = [genesis_block]
        # Unhandled transactions
        self.__open_transactions = []
        self.public_key = public_key
        self.__peer_nodes = set()
        self.node_id = node_id
        self.resolve_conflicts = False
        self.load_data()

    @property
    def chain(self):
        """ Returns a copy of the list of blocks. Should only
        use outside of the `Blockchain` class. """
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        """ Returns a copy of the list of open transactions. """
        return self.__open_transactions[:]

    def load_data(self):
        """ Loads and populates app data from file in hard disk. """
        try:
            with open(f'blockchain-{self.node_id}.txt', mode='r') as f:
                file_content = f.readlines()
                # eliminate the \n' at the end of line by using [:-1]
                blockchain = json.loads(file_content[0][:-1])
                open_transactions = json.loads(file_content[1][:-1])

                updated_blockchain = []
                for block in blockchain:
                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                         for tx in block['transactions']],
                        block['proof'],
                        block['timestamp']
                    )
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain

                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions

                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            pass
        finally:
            print('Clean up.')

    def save_data(self):
        """ Saves current app data into a file that will persist in the hard disk.

        The data is saved in the form of separate line of JSONs
        """
        try:
            with open(f'blockchain-{self.node_id}.txt', mode='w') as f:
                # Method 1: use the to_deep_dict() to convert each block to a form
                # that can be dumped as JSON
                # saveable_chain = [block.to_deep_dict() for block in blockchain]
                # Method 2: use nested listcomp like below
                saveable_chain = [block.__dict__ for block in
                                  [Block(
                                      block_el.index,
                                      block_el.previous_hash,
                                      [tx.__dict__ for tx in block_el.transactions],
                                      block_el.proof,
                                      block_el.timestamp)
                                   for block_el in self.__chain]
                                  ]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
        except IOError:
            print('Saving app data failed.')

    def proof_of_work(self):
        """ Finds a 'proof-of-work' number for a newly being mined block.

        A 'proof-of-work' makes the hash of
        current open transactions,
        hash of the last block,
        and this proof of work number itself
        satify the difficulty criteria.
        This 'proof-of-work' is then added to the new block to be mined. This hash value
        helps secure the blockchain from any cheat of modifying the previous blocks'
        :previous_hash: and/or :transactions:.

        Returns:
            The found proof of work number
        """
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self, sender=None):
        """ Calculates the current account balance the `sender` has.

        Arguments:
            sender (`str`, default to `None`): The account (public key) for which balance is calculated.
                If the passed-in value is `None` the method will calculate the account balance
                of the `self.public_key` node.

        Returns:
            `None` if the `sender` argument is `None` and `public_key` (the `public_key`
                is also the wallet's `public key`) is `None`.
            Otherwise return the result of substracting the total amount sent from the
                total amount received.
        """
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
        # Amounts sent in the past (already mined and put in blockchain blocks)
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender ==
                      participant] for block in self.__chain]
        # Amounts will be sent in the future (saved in the open_transactions)
        open_tx_sender = [
            tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        # Amounts received in the past (already finalized and put in blockchain blocks)
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient ==
                         participant] for block in self.__chain]
        # Note that amounts from MINING_REWARD will only be available when a mining is done

        # Calculate the balance by flattening the 2 lists of lists,
        # then sum up elements in the flatten lists
        return sum([el for row in tx_recipient for el in row]) - sum([el for row in tx_sender for el in row])

    def get_last_blockchain_value(self):
        """ Gets the last block value from the blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, sender, recipient, signature, amount=1.0, is_receiving=False):
        """ Appends a new transaction value as well as the last blockchain value
            to the blockchain.

        Arguments:
            sender (`str`): The sender of the coins.
            recipient (`str`): The recipient of the coins.
            signature (`str`): The signature of the transaction.
            amount (`float` default = 1.0): The amount of coins sent with the transaction.
            is_receiving (`bool`): Flag indicating whether the transaction to be added
                is received from broadcast.

        Returns:
            True if the transaction was add successfully, False otherwise.
        """
        # if self.public_key == None:
        #     return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = f'http://{node}/broadcast-transaction'
                    try:
                        response = requests.post(
                            url, json=transaction.__dict__)
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined, needs resolving')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def mine_block(self):
        """ Puts all open transactions into a new block then chains that block into the blockchain.

        Returns:
            The :obj:`Block` mined if the whole process of mining block was successful, None otherwise.
        """
        if self.public_key == None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # The mining transaction is not signed (pass in signature as empty str)
        reward_transaction = Transaction(
            'MINING', self.public_key, '', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        # Broadcasting the newly added block to other nodes
        for node in self.__peer_nodes:
            url = f'http://{node}/broadcast-block'
            converted_block = block.__dict__.copy()
            converted_block['transactions'] = [
                tx.__dict__ for tx in converted_block['transactions']]
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving.')
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return block

    def add_block(self, block):
        """ Adds a new block received from block broadcasting to the blockchain.

        Arguments:
            block (`dict`): The JSON format block to be added.

        Returns:
            True if adding the block succeeds, False otherwise.
        """
        transactions = [Transaction(
            tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
            for tx in block['transactions']]
        # Note that we exclude the last transaction (which is the MINING reward)
        # when verify the proof-of-work
        proof_is_valid = Verification.valid_proof(
            transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        converted_block = Block(
            block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        # Update open transactions on the peer node when a new broadcast block is added
        stored_transactions = self.__open_transactions[:]
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if (opentx.sender == itx['sender'] and
                    opentx.recipient == itx['recipient'] and
                    opentx.amount == itx['amount'] and
                        opentx.signature == itx['signature']):
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Transaction was already removed.')
        self.save_data()
        return True

    def resolve(self):
        """ Resolves conflicts of blockchains among the node owning this blockchain and
        its other peer nodes. This is also called making `consensus` between nodes.

        The rule for resolving conflicts is:
            (1) Letting the longest valid blockchain win by replacing the current blockchain
            with that winner one.
        """
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = f'http://{node}/chain'
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(
                    block['index'],
                    block['previous_hash'],
                    [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                     for tx in block['transactions']],
                    block['proof'],
                    block['timestamp']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(winner_chain)
                print(f'node_chain_length: {node_chain_length}')
                print(f'local_chain_length: {local_chain_length}')
                if node_chain_length > local_chain_length and Verification.verify_chain(node_chain):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                print(
                    'Error while sending request GET /chain to resolve blockchain conflicts...')
                print(requests.exceptions.ConnectionError.message)
                continue
        self.resolve_conflicts = False
        self.chain = winner_chain
        if replace:
            self.__open_transactions = []
        self.save_data()
        return replace

    def add_peer_node(self, node):
        """ Adds a new node to the peer node set.

        Arguments:
            node: The node URL which should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """ Removes a node from the peer node set.

        Arguments:
            node: The node URL which should be removed.
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """ Returns a list of all connected peer nodes. """
        return list(self.__peer_nodes)[:]
