import base64
import getpass
from cryptography.fernet import Fernet
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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
    encrypt_vault('senha')