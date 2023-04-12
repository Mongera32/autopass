# Importing required module
import subprocess
# import required module
import getpass
import hashlib
import base64
from cryptography.fernet import Fernet

def string_encrypt(message, password):
    # Define the password and salt
    password = b"password"
    salt = b"my_salt"

    # Use PBKDF2 to derive the key from the password and salt
    kdf = hashlib.pbkdf2_hmac("sha256", password, salt, 100000)

    # Use the derived key to create a Fernet object
    key = base64.urlsafe_b64encode(kdf)
    fernet = Fernet(key)

    # Define the string to be encrypted
    message = "This is a secret message"

    # Convert the string to bytes
    message_bytes = message.encode()

    # Encrypt the bytes using Fernet
    encrypted_bytes = fernet.encrypt(message_bytes)

    # Convert the encrypted bytes to a string
    encrypted_message = encrypted_bytes.decode()

    print("Original message:", message)
    print("Encrypted message:", encrypted_message)

    return password, salt, encrypted_message

def get_key(timid = True):

    key1=0
    key2=1
    while key1!=key2:

        key1 = getpass.getpass(prompt='Please input your encryption key: ', stream=None)

        if timid: key2 = getpass.getpass(prompt='Warning: If you forget your key, the passwords inside the vault will be lost! Please confirm your key: ', stream=None)
        else: key2 = key1

    return key1


def get_login():
    service = input(prompt='Please input your login associated to the service (example: Victor.silva@gmail.com): ')
    return service

def get_service():
    login = input(prompt='Please input the name of the service that want to save your password for (example: e-mail): ')
    return login

def decrypt_csv(key):
    try:
        subprocess.run(f'ccdecrypt --key {key} vault.csv', shell=True)
        return True
    except:
        print('File not found. Please check if it is encrypted and in the current directory')
        return False


def ferencrypt(key):
    f = Fernet(key)
    with open('vault.csv', "rb") as file:
        # read the encrypted data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open('vault.csv', "wb") as file:
        file.write(encrypted_data)

def encrypt_csv(key):
    try:
        subprocess.run(f'ccencrypt --key {key} vault.csv', shell=True)
        return True
    except:
        print('File not found. Please check if it is decrypted and in the current directory')
        return False

ferencrypt('nhf8923hf89233f2io')

if __name__ == "__main__":
    string_encrypt("meu texto secreto", "minha senha")
