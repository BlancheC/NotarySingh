#Author: Blanche Chung
#Created Date: Spring 2023
#Description: This file encrypting and decrypting data
# Needs to be intergrated

from cryptography.fernet import Fernet

class SecureStorage:
    def __init__(self, key=None):
        if key:
            self.key = key
        else:
            self.key = Fernet.generate_key()

    def encrypt(self, data):
        f = Fernet(self.key)
        encrypted_data = f.encrypt(data.encode('utf-8'))
        return encrypted_data

    def decrypt(self, encrypted_data):
        f = Fernet(self.key)
        decrypted_data = f.decrypt(encrypted_data).decode('utf-8')
        return decrypted_data

    def save_key(self, key_file):
        with open(key_file, 'wb') as f:
            f.write(self.key)

    def load_key(self, key_file):
        with open(key_file, 'rb') as f:
            self.key = f.read()