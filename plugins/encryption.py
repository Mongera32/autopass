import base64
from cryptography.fernet import Fernet
import hashlib
import pandas as pd

def fernet_gen(master_pw:str):
    """Derives a fernet key from "password" string, instantiates a "fernet" object and then returns this object. """

    # Define the password and salt
    master_pw = master_pw.encode()
    salt = b"my_salt"

    # Use PBKDF2 to derive the key from the password and salt
    kdf = hashlib.pbkdf2_hmac("sha256", master_pw, salt, 100000)

    # Use the derived key to create a Fernet object
    key = base64.urlsafe_b64encode(kdf)
    fernet = Fernet(key)

    return fernet

def string_encrypt(message:str, master_pw:str):
    """
    Encrypts "massage" using a fernet key derived from the given master password.
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

def string_decrypt(enc_message:bytes, master_pw:str):
    """
    Decrypts "enc_massage" using a fernet key derived from the given master password.
    """

    # generate fernet object from password
    fernet = fernet_gen(master_pw)

    # returns encrypted message to original byte sequence
    byte_message = fernet.decrypt(enc_message)

    message = byte_message.decode()

    return message

def df_enc(df:pd.DataFrame, master_pw:str) -> pd.DataFrame:
    """Encrypts all heads and values in the DataFrame "df" and updates them"""

    # Encrypting column names
    col1 = df.columns[0]
    col2 = df.columns[1]
    enc_col1 = string_encrypt(col1,master_pw)
    enc_col2 = string_encrypt(col2,master_pw)

    # creating columns with encrypted heads
    df[enc_col1] = df['login']
    df[enc_col2] = df['password']

    # removing old columns
    df = df.drop(labels=['login','password'], axis=1)

    # decrypting columns
    df[enc_col1] = df[enc_col1].apply(string_encrypt,args=(master_pw,))
    df[enc_col2] = df[enc_col2].apply(string_encrypt,args=(master_pw,))

    return df

def df_dec(df:pd.DataFrame, master_pw:str) -> pd.DataFrame:
    """
    Decrypts all values in the DataFrame "df" and updates them.
    If the master password input is wrong, displays a warning and returns the original encrypted df.
    """

    # decrypt column names
    enc_col1 = df.columns[0]
    enc_col2 = df.columns[1]
    byte_enc_col1 = eval(enc_col1)
    byte_enc_col2 = eval(enc_col2)
    col1 = string_decrypt(byte_enc_col1,master_pw)
    col2 = string_decrypt(byte_enc_col2,master_pw)

    # Checking if password is incorrect
    if (col1 != 'login' or col2 != 'password'):
        print('Master password is incorrect')
        return df, True

    #creating columns with decrypted heads
    df['login'] = df[enc_col1]
    df['password'] = df[enc_col2]

    #removing old columns
    df = df.drop(labels=[enc_col1,enc_col2], axis=1)

    #turning values from string to bytes
    df['login'] = df['login'].apply(lambda x : eval(x))
    df['password'] = df['password'].apply(lambda x : eval(x))

    # decrypting columns
    df['login'] = df['login'].apply(string_decrypt,args=(master_pw,))
    df['password'] = df['password'].apply(string_decrypt,args=(master_pw,))

    return df, False

if __name__ == "__main__":
    pass
