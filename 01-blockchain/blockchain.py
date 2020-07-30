import json

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
        self.load_data()

    @property
    def chain(self):
        """ Return a copy of the list of blocks. Should only
        use outside of the `Blockchain` class. """
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        """ Return a copy of the list of open transactions. """
        return self.__open_transactions[:]

    def load_data(self):
        """ Load and populate app data from file in hard disk. """
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
        """ Save current app data into a file that will persist in the hard disk.

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
        """ Find a 'proof-of-work' number for a newly being mined block.

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

    def get_balance(self, participant=None):
        """ Calculate the current account balance the :participant: has.

        Arguments:
            participant (default `None`): The account for which balance is calculated.
                If the passed-in value is `None` the method will calculate the account
                balance for the `self.public_key`.

        Returns: None if the `public_key` (the `public_key` is also the wallet's `public key`) is None.
            Otherwise return the result of substracting the total amount sent from the total amount received.
        """
        if self.public_key == None:
            return None
        participant = self.public_key if participant is None else participant
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
        """ Get the last block value from the blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, sender, recipient, signature, amount=1.0):
        """ Append a new transaction value as well as the last blockchain value
            to the blockchain.

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :signature: The signature of the transaction.
            :amount: The amount of coins sent with the transaction (default = 1.0)

        Returns:
            True if the transaction was add successfully, False otherwise.
        """
        if self.public_key == None:
            return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        """ Put all open transactions into a new block then chain that block into the blockchain.

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
        return block

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
