# digital_signature.py
# Author: Blanche Chung
# Created Date: Spring 2023
# Description: This file contains functions to create and verify digital signatures
# Needs to be intergrated

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

# Generates a private key for signing documents
def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key

# Generates a public key from the given private key
def generate_public_key(private_key):
    public_key = private_key.public_key()
    return public_key

# Signs the given document using the private key
def sign_document(document, private_key):
    signature = private_key.sign(
        document,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

# Verifies the signature of a given document using the public key
def verify_signature(document, signature, public_key):
    try:
        public_key.verify(
            signature,
            document,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        return False
