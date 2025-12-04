
from phe import paillier

# 
# Generate Paillier keypair
#
def generate_keypair(n_length=512):
    """
        Generate a Paillier keypair with the specified key length.
        Returns the public and private keys.
    """
    public_key, private_key = paillier.generate_paillier_keypair(n_length=n_length)
    return public_key, private_key