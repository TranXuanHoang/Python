# Initialize a blockchain as a list
blockchain = []


def get_last_blockchain_value():
    """ Get the last block value from the blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction=[1]):
    """ Append a new transaction value as well as the last blockchain value
        to the blockchain.

    Arguments:
        :transaction_amount: The amount that should be added.
        :last_transaction: The last blockchain transaction (default [1]).
    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def print_blockchain_elements():
    """ Print out all blocks in the blockchain. """
    for index, block in enumerate(blockchain):
        print(str(index) + ">>> " + str(block))


def get_transaction_value():
    """ Return user input as a float. """
    return float(input('Your transaction amount please: '))


def get_user_choice():
    """ Return user choice as a string. """
    return input('Your choice: ')


def verify_chain():
    """ Check whether all blocks contain consistent data.

    Returns:
        True if all blocks' data is consistent, False otherwise.
    """
    for index in reversed(range(len(blockchain))):
        if index >= 1 and blockchain[index][0] != blockchain[index - 1]:
            return False
    return True


while True:
    print('Please choose an option')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('h: Change the first block')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        break
    else:
        print('Invalid option!')
    if not verify_chain():
        print('Invalid blockchain!')
        break
