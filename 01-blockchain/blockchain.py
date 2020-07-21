# Genesis block
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}

# Initialize a blockchain as a list
blockchain = [genesis_block]
open_transactions = []
owner = 'Hoang'


def hash_block(last_block):
    """ Hash the given :last_block: and return that hash value.

    Arguments:
        :last_block: the block to be hashed
    """
    return '-'.join([str(last_block[key]) for key in last_block])


def get_last_blockchain_value():
    """ Get the last block value from the blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(sender, recipient, amount=1.0):
    """ Append a new transaction value as well as the last blockchain value
        to the blockchain.

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: The amount of coins sent with the transaction (default = 1.0)
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)


def mine_block():
    """ Put all open transactions into a new block then chain that block into the blockchain. """
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': [transaction for transaction in open_transactions]
    }
    blockchain.append(block)
    open_transactions.clear()


def print_blockchain_elements():
    """ Print out all blocks in the blockchain. """
    print('=' * 50)
    for index, block in enumerate(blockchain):
        print(str(index) + ">>> " + str(block))
    else:
        print('_' * 50)
        print(blockchain)
        print('=' * 50)


def get_transaction_value():
    """ Return user input as a tuple. """
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient, tx_amount


def get_user_choice():
    """ Return user choice as a string. """
    return input('Your choice: ')


def verify_chain():
    """ Check whether all blocks contain consistent data.

    Returns:
        True if all blocks' data is consistent, False otherwise.
    """
    for index, block in enumerate(blockchain):
        if index >= 1 and block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True


while True:
    print('Please choose an option')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(owner, recipient, amount=amount)
        print('_' * 50)
        print('Current open transactions:')
        print(open_transactions)
        print('_' * 50)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{
                    'sender': 'Hoang',
                    'recipient': 'Hacker',
                    'amount': 1000
                }]
            }
    elif user_choice == 'q':
        break
    else:
        print('Invalid option!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
