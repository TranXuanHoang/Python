from time import time

from printable import Printable


class Block(Printable):
    """ Represent each block in the blockchain. """

    def __init__(self, index, previous_hash, transactions, proof, timestamp=None):
        """
        Constructor.

        Arguments:
            index (`int`): The index of the block counting from 0 for the genesis block
                and being incresed by 1 each time a new block is added to the blockchain.
            previous_hash (`str`): The hash of the previous block.
            transactions (:obj:`list` of :obj:`Transaction`s): The transactions of the new
                block to be validated (excluding the MINING block).
            proof (`int`): A number (also call a 'proof-of-work number' or a 'nonce') used
                together with the :transactions: and :last_hash: to yield a new hash
                that suffices a condition defined by the creator(s) of the blockchain.
            timestamp (`float`, optional): The timestamp in seconds since the Epoch when the
                block was added to the blockchain.
        """
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time() if timestamp is None else timestamp
        self.transactions = transactions
        self.proof = proof

    def to_deep_dict(self):
        """ Convert the entire block object to a dictionary in which the `transactions` list
        is also an array of dictionaries. So this method could be seen as returning a deep copy
        of the block object as a dictionary. """
        block = self.__dict__.copy()
        block['transactions'] = [tx.to_ordered_dict().copy()
                                 for tx in block['transactions']]
        return block
