from utility.hash_util import hash_block, hash_string_256


class Verification:
    """ Provide utility methods for verifying the integrity of
    `block`s, `transaction`s and the whole `blockchain`. """

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """ Validate whether a new block fulfills the difficulty criteria.

        Arguments:
            transactions (:obj:`list` of `Transaction`s): The transactions of the new block
                to be validated (excluding the MINING block).
            last_hash (`str`): The hash of the previous (last) block.
            proof (`int`): A number (also call a 'proof-of-work number' or a 'nonce') used
                together with the :transactions: and :last_hash: to yield a new hash
                that suffices a condition defined by the creator(s) of the blockchain.

        Returns:
            True if the difficulty criteria satify, Fals otherwise.
        """
        guess = (str([tx.to_ordered_dict() for tx in transactions]) +
                 str(last_hash) + str(proof)).encode('utf-8')
        guess_hash = hash_string_256(guess)
        return guess_hash[0:2] == '00'

    @classmethod
    def verify_chain(cls, blockchain):
        """ Check whether all blocks contain consistent data.

        Arguments:
            blockchain (:obj:`list` of `Block`s): The `blockchain` to be verified.

        Returns:
            True if all blocks' data is consistent, False otherwise.
        """
        for index, block in enumerate(blockchain):
            if index >= 1 and block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if index >= 1 and not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance):
        """ Verify whether the remaining balance is enough for a given :transaction to be made.

        Parameters:
            transaction (`Transaction`): The transaction to be verified.
            get_balance (`function`): The address of the function calculating the account balance.

        Returns:
            True if the transaction can be made, False otherwise.
        """
        # Note that, we can just call get_balance() without passing the transaciton.sender
        # argument as that is the default case when the sender is the user of this hosting node.
        return get_balance(transaction.sender) >= transaction.amount

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """ Verify whether all open transactions are valid.

        Parameters:
            open_transactions (:obj:`list` of `Transaction`s): The transactions to be verified.
            get_balance (`function`): The address of the function calculating the account balance.

        Returns:
            True if all transactions are valid, False otherwise.
        """
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
