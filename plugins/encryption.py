import base64
import getpass
from cryptography.fernet import Fernet
import os
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def fernet_gen(password:str):
        # Define the password and salt
    password = password.encode()
    salt = b"my_salt"

    # Use PBKDF2 to derive the key from the password and salt
    kdf = hashlib.pbkdf2_hmac("sha256", password, salt, 100000)

    # Use the derived key to create a Fernet object
    key = base64.urlsafe_b64encode(kdf)
    fernet = Fernet(key)

    return fernet

def string_encrypt(message:str, password:str):

    # generate fernet object from password
    fernet = fernet_gen(password)

    # Convert the string to bytes
    bytecode = message.encode()

    # Encrypt the bytes using Fernet
    enc_message = fernet.encrypt(bytecode)

    return enc_message

def string_decrypt(enc_message, password:str):

    # generate fernet object from password
    fernet = fernet_gen(password)

    # returns encrypted message to original byte sequence
    byte_message = fernet.decrypt(enc_message)

    message = byte_message.decode()

    return message

def keygen(master_password:str):
    """Derives a Fernet key object from a master password"""

    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
)
    b_password = master_password.encode('utf-8')

    key = Fernet(
          base64.urlsafe_b64encode(
          kdf.derive( b_password
)))

    return key

def input_key(timid = True):

    key1=0
    key2=1
    while key1!=key2:

        key1 = getpass.getpass(prompt='Please input your encryption key: ', stream=None)

        if timid: key2 = getpass.getpass(prompt='Warning: If you forget your master password, the passwords inside the vault will be lost! Please confirm your key: ', stream=None)
        else: key2 = key1

    return key1


def input_login():
    service = input(prompt='Please input your login associated to the service (example: Victor.silva@gmail.com): ')
    return service

def input_service():
    login = input(prompt='Please input the name of the service that want to save your password for (example: e-mail): ')
    return login

def update_vault(encrypt = True):


    vault = open('vault.csv', 'w+')

    teste = vault.read()

    #vault.write('encrypted')

    #vault.close()

    print(teste)
    vault.close()
    return teste

def encrypt_vault(master_password):
    """Encrypts vault.csv"""

    key = keygen(master_password)
    encrypted = ''

    with open('vault.csv', 'rb') as unencrypted:
        _file = unencrypted.read()
        encrypted = key.encrypt(_file)

    with open('vault.csv', 'w') as encrypted_file:
        encrypted_file.write(str(encrypted))

    return None

def decrypt_vault(master_password):
    key = keygen(master_password)
    print = type(key)
    with open('vault.csv', 'r') as encrypted_file:
        _file = (encrypted_file.read())
        decrypted = key.decrypt(_file)
    print(decrypted)
    return decrypted


if __name__ == "__main__":
    pass
