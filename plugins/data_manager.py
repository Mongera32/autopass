from plugins.pandas_functions import search_login, read_file, check_for_duplicates
import pyperclip
from plugins.randomizer import random_sequence
from plugins.encryption import encrypt_csv, get_key, get_login, decrypt_csv

def getpw(login):
    """fecthes a password from vault"""

    df = read_file()

    filter = df['login'] == login
    password = df[filter].iloc[0]['password']
    password.strip('\'')
    password

    pyperclip.copy(password)

def update_df(index, login, df, password):

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

def addpw(login):
    """stores a password in the vault"""

    password = random_sequence()

    df = read_file()

    index = len(df)

    update_df(index, login, df, password)

    pyperclip.copy(password)

    return None

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

    return None
