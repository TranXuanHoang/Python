import json

from block import Block
from hash_util import hash_block
from transaction import Transaction
from verification import Verification

# Number of coins rewarded for each mining
MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_id):
        # Genesis block
        # Note that, for the genesis block, proof can be initialized with any value
        genesis_block = Block(index=0, previous_hash='',
                              transactions=[], proof=100, timestamp=0)
        # Initialize a blockchain as a list
        self.__chain = [genesis_block]
        # Unhandled transactions
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    def get_chain(self):
        """ Return a copy of the list of blocks. """
        return self.__chain[:]

    def get_open_transactions(self):
        """ Return a copy of the list of open transactions. """
        return self.__open_transactions[:]

    def load_data(self):
        """ Load and populate app data from file in hard disk. """
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                # eliminate the \n' at the end of line by using [:-1]
                blockchain = json.loads(file_content[0][:-1])
                open_transactions = json.loads(file_content[1])

                updated_blockchain = []
                for block in blockchain:
                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        [Transaction(tx['sender'], tx['recipient'], tx['amount'])
                         for tx in block['transactions']],
                        block['proof'],
                        block['timestamp']
                    )
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain

                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except (IOError, IndexError):
            pass
        finally:
            print('Clean up.')

    def save_data(self):
        """ Save current app data into a file that will persist in the hard disk.

        The data is saved in the form of separate line of JSONs
        """
        try:
            with open('blockchain.txt', mode='w') as f:
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
                balance for the `self.hosting_node`.

        Returns: the result of substracting the total amount sent from the total amount received.
        """
        participant = self.hosting_node if participant is None else participant
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

    def add_transaction(self, sender, recipient, amount=1.0):
        """ Append a new transaction value as well as the last blockchain value
            to the blockchain.

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :amount: The amount of coins sent with the transaction (default = 1.0)

        Returns:
            True if the transaction was add successfully, False otherwise.
        """
        transaction = Transaction(sender, recipient, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        """ Put all open transactions into a new block then chain that block into the blockchain.

        Returns:
            True if the whole process of mining block was successful, False otherwise.
        """
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction(
            'MINING', self.hosting_node, MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True
