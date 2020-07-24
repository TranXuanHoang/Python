import hashlib
import json


def hash_string_256(string):
    """ Hash a given input :string: using SHA256 algorithm. """
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """ Hash the given :block: and return that hash value.

    Arguments:
        :block: the block to be hashed
    """
    return hash_string_256(json.dumps(block, sort_keys=True).encode('utf-8'))
