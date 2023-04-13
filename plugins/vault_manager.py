from plugins.pandas_functions import search_login, read_file, check_for_duplicates, update_df, search_index
import pyperclip
from plugins.pw_generator import random_sequence
from plugins.encryption import string_decrypt, string_encrypt, columns_decrypt, columns_encrypt
from inputs import input_pw, input_login, input_service

def getpw():
    """fecthes a password from the encrypted vault"""

    # asking for login and generating password
    master_pw = input_pw(timid=False)
    login = input_login()

    # turning vault.csv into a dataframe
    df = read_file()

    #decrypting columns
    df = columns_decrypt(df,master_pw)

    # searching for correspondent password in the "password " column
    filter = df['login'] == login
    password = df[filter].iloc[0]['password']
    password = password.strip('\'')

    pyperclip.copy(password)

    # encrypting columns again
    df["login"] = df["login"].apply(string_encrypt,args=(master_pw,))
    df["password"] = df["password"].apply(string_encrypt,args=(master_pw,))

    return None

def updatepw():
    """updates a password in the vault"""

    master_pw = input_pw()
    login = input_login()
    password = random_sequence()

    df = read_file()

    index = search_index(login)
    if index == None:
        print('login not found. dataframe not updated')
        return None

    update_df(index, login, df, password)

    pyperclip.copy(password)

    return None

def addpw():
    """
    - Asks user for a login \n
    - Generates a random password \n
    - Encrypts both and stores them in the vault \n
    - Sends generated password to clipboard
    """

    # asking for login and generating password
    master_pw = input_pw()
    login = input_login()
    password = random_sequence()

    pyperclip.copy(password)

    # encrypting login and password:
    enc_login = string_encrypt(login,master_pw)
    enc_password = string_encrypt(password,master_pw)

    # defining arguments for update_df function
    df = read_file()
    index = len(df)

    update_df(index, enc_login, df, enc_password)

    return None

def lock_vault():
    """Encrypts all strings in the vault"""

    # turning vault.csv into a dataframe
    df = read_file()

    # applying encryption in all elements
    df = df.apply(string_encrypt)

def unlock_vault():
    """Unencrypts all passwords and logins in the vault"""
    pass

def operation_manager(cmd = 'getpw'):

    if cmd=='encrypt': timid=True
    else: timid = False
    key = get_key(timid)

    if cmd == 'encrypt':
        encrypt_csv(key)
        return None
    if cmd == 'decrypt':
        decrypt_csv(key)
        return None

    login = get_login()

    decrypt_csv(key)
    try:
        cmd += f'(\'{login}\')'
        eval(cmd)
    except:
        encrypt_csv(key)
    encrypt_csv(key)

    pass

if __name__ == "__main__":
    addpw()
