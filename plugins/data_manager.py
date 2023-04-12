from plugins.pandas_functions import search_login, read_file, check_for_duplicates
import pyperclip
from plugins.randomizer import random_sequence
from plugins.encryption import string_decrypt, string_encrypt, input_pw


def input_login():
    """Asks user to imput their login"""
    service = input('Please input your login associated to the service (example: victor.silva@gmail.com): ')
    return service

def input_service():
    """Asks user to imput the service"""
    login = input(prompt='Please input the name of the service that want to save your password for (example: gmail,): ')
    return login

def getpw(login):
    """fecthes a password from the encrypted vault"""
    # asking for user login
    login = input_login()

    # turning vault.csv into a dataframe
    df = read_file()

    # decrypting column
    df["login"] = df["login"].apply(string_decrypt)

    # searching for correspondent password in the "password " column
    filter = df['login'] == login
    password = df[filter].iloc[0]['password']
    password = password.strip('\'')

    pyperclip.copy(password)

def update_df(index, login, df, password):
    """
    Inserts a row in a DataFrame or updates an existing row \n
    - index: \n
    Index of the row to be updated. Must be equal to the length of the DataFrame ( len(df) ) for this function to insert a new row. \n

    - login \n
    Login associated to the password \n

    - df \n
    Dataframe extracted from vault.csv \n

    - password \n
    Password to be inserted. \n
    """


    df.at[index,'login'] = login
    df.at[index,'password'] = password

    if check_for_duplicates(login,df):
        print('duplicate login found. Dataframe not updated')
        return None
    df.to_csv(path_or_buf = 'vault.csv', index = False, sep = " ")
    return None

def updatepw(login):
    """updates a password in the vault"""

    password = random_sequence()

    df = read_file()

    index = search_login(login).index[0]
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

    # encrypting login and password:
    enc_login = string_encrypt(login,master_pw)
    enc_master_pw = string_encrypt(login,master_pw)

    # defining arguments for update_df function
    df = read_file()
    index = len(df)

    update_df(index, enc_login, df, enc_master_pw)

    pyperclip.copy(password)

    return None

def lock_vault():
    """Encrypts all strings in the vault"""



    # turning vault.csv into a dataframe
    df = read_file()

    # applying encryption in all elements
    df = df.apply(string_encrypt)


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
