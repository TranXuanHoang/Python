from Crypto.PublicKey import RSA
import Crypto.Random
import binascii


class Wallet:
    """ Represent a cryptocurrency wallet possessed by each node of the blockchain network.

    Each wallet can be seen as a pair of public and private keys. The public key
    is then used as the `sender` of every `transaction` made by the wallet owner.
    The private key, on the other hand, should be kept private and will only be
    used to check whether all open transactions were not tampered or modified.

    Attributes:
        private_key (`str`): The private key of the wallet.
        public_key (`str`): The public key of the wallet.
    """

    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        """ Generate a pair of private and public keys and populate them to the wallet. """
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_key(self):
        """ Save the private and public keys to a file for later uses.
        This is only for demonstration of persisting keys in this example.
        In the real world applications, we should not save keys like this. """
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet.txt', mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
            except (IOError, IndexError):
                print('Saving wallet failed...')

    def load_keys(self):
        """ Load both the private and public keys from a file used in saving them before. """
        try:
            with open('wallet.txt', mode='r') as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
        except (IOError, IndexError):
            print('Loading wallet failed...')

    def generate_keys(self):
        """ Generate and return a tuple of private and public keys (both are in string).
        RSA is the algorithm used in here for generating the keys. """
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')