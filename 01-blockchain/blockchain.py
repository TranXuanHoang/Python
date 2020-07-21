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

# Set of senders, recipients participated in transactions
participants = set([owner])


def hash_block(block):
    """ Hash the given :block: and return that hash value.

    Arguments:
        :block: the block to be hashed
    """
    return '-'.join([str(block[key]) for key in block])


def get_balance(participant):
    """ Calculate the current account balance the :participant: has.

    Returns: the result of substracting the total amount sent from the total amount received.
    """
    # Amounts sent in the past (already mined and put in blockchain blocks)
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    # Amounts will be sent in the future (saved in the open_transactions)
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    # Amounts received in the past (already finalized and put in blockchain blocks)
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    # Note that amounts from MINING_REWARD will only be available when a mining is done

    # Calculate the balance by flattening the 2 lists of lists,
    # then sum up elements in the flatten lists
    return sum([el for row in tx_recipient for el in row]) - sum([el for row in tx_sender for el in row])


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
    participants.add(sender)
    participants.add(recipient)


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
    print('4: Output participants')
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
    elif user_choice == '4':
        print(participants)
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
