import json

from block import Block
from hash_util import hash_block, hash_string_256
from transaction import Transaction

# Number of coins rewarded for each mining
MINING_REWARD = 10

# Initialize a blockchain as a list
blockchain = []
open_transactions = []
owner = 'Hoang'


def load_data():
    """ Load and populate app data from file in hard disk. """
    global blockchain
    global open_transactions
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
            blockchain = updated_blockchain

            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(
                    tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except (IOError, IndexError):
        # Genesis block
        # Note that, for the genesis block, proof can be initialized with any value
        genesis_block = Block(index=0, previous_hash='',
                              transactions=[], proof=100, timestamp=0)

        # Initialize a blockchain as a list
        blockchain = [genesis_block]
        open_transactions = []
    finally:
        print('Clean up.')


load_data()


def save_data():
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
                                  for block_el in blockchain]
                              ]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
    except IOError:
        print('Saving app data failed.')


def valid_proof(transactions, last_hash, proof):
    """ Validate whether a new block fulfill the difficulty criteria.

    Arguments:
        :transactions: The transactions of the new block to be validated
            (excluding the MINING block).
        :last_hash: The hash of the previous (last) block.
        :proof: A number (also call a 'proof-of-work number' or a 'nonce') used
            together with the :transactions: and :last_hash: to yield a new hash
            that suffices a condition defined by the creator(s) of the blockchain.
    """
    guess = (str([tx.to_ordered_dict() for tx in transactions]) +
             str(last_hash) + str(proof)).encode('utf-8')
    guess_hash = hash_string_256(guess)
    return guess_hash[0:2] == '00'


def proof_of_work():
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
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    """ Calculate the current account balance the :participant: has.

    Returns: the result of substracting the total amount sent from the total amount received.
    """
    # Amounts sent in the past (already mined and put in blockchain blocks)
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender ==
                  participant] for block in blockchain]
    # Amounts will be sent in the future (saved in the open_transactions)
    open_tx_sender = [
        tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    # Amounts received in the past (already finalized and put in blockchain blocks)
    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient ==
                     participant] for block in blockchain]
    # Note that amounts from MINING_REWARD will only be available when a mining is done

    # Calculate the balance by flattening the 2 lists of lists,
    # then sum up elements in the flatten lists
    return sum([el for row in tx_recipient for el in row]) - sum([el for row in tx_sender for el in row])


def get_last_blockchain_value():
    """ Get the last block value from the blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    """ Verify whether the remaining balance is enough for a given :transaction to be made.

    Parameters:
        :transaction: the transaction to be verified.

    Returns:
        True if the transaction can be made, False otherwise.
    """
    return get_balance(transaction.sender) >= transaction.amount


def add_transaction(sender, recipient, amount=1.0):
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
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def mine_block():
    """ Put all open transactions into a new block then chain that block into the blockchain.

    Returns:
        True if the whole process of mining block was successful, False otherwise.
    """
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True


def print_blockchain_elements():
    """ Print out all blocks in the blockchain. """
    print('=' * 50)
    for index, block in enumerate(blockchain):
        print(f'{index:>3}>>> {block}')
    else:
        print('_' * 50)
        print(blockchain)
        print('_' * 50)
        print('In JSON Format:')
        jsonizeable_chain = [block.to_deep_dict() for block in blockchain]
        print(json.dumps(jsonizeable_chain).encode('utf-8'))
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
        if index >= 1 and block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if index >= 1 and not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            return False
    return True


def verify_transactions():
    """ Verify whether all open transactions are valid.

    Returns:
        True if all transactions are valid, False otherwise.
    """
    return all([verify_transaction(tx) for tx in open_transactions])


while True:
    print('Please choose an option')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Verify all transactions')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(owner, recipient, amount=amount):
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print('_' * 50)
        print('Current open transactions:')
        print(open_transactions)
        print('_' * 50)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'q':
        break
    else:
        print('Invalid option!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
    print(f'Balance of {owner}: {get_balance(owner):6.2f}')
else:
    print('User left!')

print('Done!')
