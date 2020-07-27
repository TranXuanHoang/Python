import hashlib
import json

__all__ = ['hash_string_256', 'hash_block']


def hash_string_256(string):
    """ Hash a given input :string: using SHA256 algorithm. """
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """ Hash the given :block: and return that hash value.

    Arguments:
        :block: the block to be hashed
    """
    # Get a dictionary whose key-value pairs are attributes and values of the 'block' object.
    # Then copy that dictionary so that the hash function later on will not cause any affects
    # to the original 'block' object
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict()
                                      for tx in hashable_block['transactions']]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode('utf-8'))
