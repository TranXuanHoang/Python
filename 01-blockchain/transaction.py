from collections import OrderedDict

from utility.printable import Printable


class Transaction(Printable):
    """ Represent each transaction of sending/receiving coins. """

    def __init__(self, sender, recipient, amount):
        """ Constructor.

        Arguments:
            sender (`str`): The sender of the coins.
            recipient (`str`): The recipient of the coins.
            amount (`float`): The amount of coins sent with the transaction.
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_ordered_dict(self):
        """ Convert the transaction object into an `OrderedDict`.

        This conversion is important when hashing blocks that contain transactions.
        Without ordering the transaction objects' key:value pairs, hash values might differ
        between different hash sessions even though we hash the same block (same transactions).

        This conversion is also useful when we want to convert each block object into JSON.
        The nested transactions in each block of the blockchain can be safely converted into
        an `OrderedDict` first, and then the entire block itself will be converted to a dictionary.
        (See block.Block.to_deep_dict() for how this method is used in that coversion logic)
        """
        return OrderedDict([
            ('sender', self.sender),
            ('recipient', self.recipient),
            ('amount', self.amount)
        ])
