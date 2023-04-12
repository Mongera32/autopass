import base64
import getpass
from cryptography.fernet import Fernet
import os
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def fernet_gen(password:str):
    """Derives a fernet key from "password" string, instantiates a "fernet" object and then returns this object. """

    # Define the password and salt
    password = password.encode()
    salt = b"my_salt"

    # Use PBKDF2 to derive the key from the password and salt
    kdf = hashlib.pbkdf2_hmac("sha256", password, salt, 100000)

    # Use the derived key to create a Fernet object
    key = base64.urlsafe_b64encode(kdf)
    fernet = Fernet(key)

    return fernet

def string_encrypt(message:str, master_pw:str):
    """
    Calls input_pw to get user's password.
    Encrypts "massage" using a fernet key derived from the given password.
    """

    # getting user master password imput with confirmation
    #master_pw = input_pw(timid = True)

    # generate fernet object from password
    fernet = fernet_gen(master_pw)

    # Convert the string to bytes
    bytecode = message.encode()

    # Encrypt the bytes using Fernet
    enc_message = fernet.encrypt(bytecode)

    return enc_message

def string_decrypt(enc_message:str,master_pw):
    """
    Calls input_pw to get user's password. \n
    Decrypts "enc_massage" using a fernet key derived from the given password.
    """

    # generate fernet object from password
    fernet = fernet_gen(master_pw)

    # returns encrypted message to original byte sequence
    byte_message = fernet.decrypt(enc_message)

    message = byte_message.decode()

    return message

def input_pw(timid = True):
    """
    Asks user for a hidden "master password" imput and returns the password. \n
    Set "Timid = True" to ask user for a confirmation of the password.
    """

    # safe password imput
    password = getpass.getpass(prompt='Please input your master password: ', stream=None)

    # password confirmation if necessary
    if timid:
        confirmation = getpass.getpass(prompt='Please confirm your master password: ', stream=None)

        while password!=confirmation:
            password = getpass.getpass(prompt='Passwords do not match! Please input your master password again: ', stream=None)
            confirmation = getpass.getpass(prompt='Please confirm your master password again: ', stream=None)

    return password



if __name__ == "__main__":
    pass
