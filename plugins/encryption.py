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

def string_decrypt(enc_message, master_pw:str):
    """
    Decrypts "enc_massage" using a fernet key derived from the given master password.
    """

    # generate fernet object from password
    fernet = fernet_gen(master_pw)

    # returns encrypted message to original byte sequence
    byte_message = fernet.decrypt(enc_message)

    message = byte_message.decode()

    return message

def columns_encrypt(df, master_pw:str):
    """Encrypts all values in the DataFrame "df" and updates them"""

    # decrypting columns
    df["login"] = df["login"].apply(string_encrypt,args=(master_pw,))
    df["password"] = df["password"].apply(string_encrypt,args=(master_pw,))

    return df

def columns_decrypt(df, master_pw):
    """Decrypts all values in the DataFrame "df" and updates them"""

    # decrypting columns
    df["login"] = df["login"].apply(string_decrypt,args=(master_pw,))
    df["password"] = df["password"].apply(string_decrypt,args=(master_pw,))

    return df

if __name__ == "__main__":
    df = pd.read_csv('vault.csv', sep = " ")
    master_pw = 'senhasenha'
    df_original = df.copy()

    print(df_original)

    columns_encrypt(df,master_pw)
    print(df)

    columns_decrypt(df, master_pw)

    print(df_original == df)
