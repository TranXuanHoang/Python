import json

from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet


class Node:
    """ Initialize starting point of the app and provide UI for interacting with users.

    Attributes:
        wallet (:obj:`Wallet`): A wallet that has a pair of public and private keys.
            The public key is used as a unique user ID of the sender of every transactions
            made by this node user.
        blockchain (:obj:`Blockchain`): An instance of the `Blockchain` class containing
            all state of the blockchain and transactions as well as its processing logic methods.
    """

    def __init__(self):
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_transaction_value(self):
        """ Return user input as a tuple. """
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Your transaction amount please: '))
        return tx_recipient, tx_amount

    def get_user_choice(self):
        """ Return user choice as a string. """
        return input('Your choice: ')

    def print_blockchain_elements(self):
        """ Print out all blocks in the blockchain. """
        print('=' * 50)
        for index, block in enumerate(self.blockchain.chain):
            print(f'{index:>3}>>> {block}')
        else:
            print('_' * 50)
            print(self.blockchain.chain)
            print('_' * 50)
            print('In JSON Format:')
            jsonizeable_chain = [block.to_deep_dict()
                                 for block in self.blockchain.chain]
            print(json.dumps(jsonizeable_chain).encode('utf-8'))
            print('=' * 50)

    def listen_for_input(self):
        while True:
            print('Please choose an option')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Verify all transactions')
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save keys')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(self.wallet.public_key, recipient, amount=amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed!')
                print('_' * 50)
                print('Current open transactions:')
                print(self.blockchain.get_open_transactions())
                print('_' * 50)
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed. Got no wallet?')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_key()
            elif user_choice == 'q':
                break
            else:
                print('Invalid option!')
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                break
            print(
                f'Balance of {self.wallet.public_key}: {self.blockchain.get_balance():6.2f}')
        else:
            print('User left!')

        print('Done!')


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
