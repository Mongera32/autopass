from plugins.pandas_functions import search_login, read_file, check_for_duplicates, update_df, search_index, override_file, create_file
import pyperclip
from plugins.pw_generator import random_sequence
from plugins.encryption import string_decrypt, string_encrypt, df_dec, df_enc
from inputs import input_pw, input_login, input_service

def getpw():
    """fetches a password from the encrypted vault"""

    # asking for login and generating password
    master_pw = input_pw(timid=False)
    login = input_login()

    # turning vault.csv into a dataframe
    df = read_file()

    #decrypting columns
    df = df_dec(df,master_pw)
    print(df)
    print(type(df))

    # searching for correspondent password in the "password " column
    filter = df['login'] == login
    password = df[filter].iloc[0]['password']

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

    # retrieving dataframe from vault.csv
    df = read_file()

    # Receiving master password input
    master_pw = input_pw(timid=False)

    # Decrypting DataFrame
    df, wrong_master_pw = df_dec(df,master_pw)

    # Aborts operation if master password is wrong
    if wrong_master_pw: return None


    # asking for login and generating password
    login = input_login()
    password = random_sequence()

    # aborts operation if duplicates are found
    check = check_for_duplicates(login,df)
    if check:
        print("duplicate login found. Aborting")
        return None

    # updating the vault.csv file with an appended login and password
    update_df(df,
              len(df),
              login,
              password
)
    #encrypting DataFrame
    df = df_enc(df,master_pw)

    # updating vault.csv
    override_file(df)

    # sending password to clipboard
    pyperclip.copy(password)

    return None

def lockvault():
    """Encrypts all data in the vault.csv file"""

    # read file
    df = read_file()

    # get credentials
    master_pw = input_pw(timid=True)

    # encrypt all data
    df = df_enc(df,master_pw)

    # update vault.csv
    override_file(df)

    return None

def unlockvault():
    """Decrypts all data in the vault.csv file"""

    # confirmation
    answer = input('You are about to decrypt all data in your vault, leaving it exposed should someone have access to your computer. Proceed anyways? [y/n]')
    if answer != 'y':
        print('Vault was not decrypted')
        return None
    else:
        print('Proceeding with vault decryption')

    # read file
    df = read_file()

    # get credentials
    master_pw = input_pw(timid=False)

    # decrypt all data
    df = df_dec(df,master_pw)

    # update vault.csv
    try: override_file(df)
    except AttributeError:
        print('Vault is empty. Nothing to unlock')
        return None

    return None

def set_vault():
    """Sets up the vault.csv file that will be used to store the passwords. If it already exists, asks user for extra confirmation"""

    # checking of vault.csv already exists
    file_exists = True
    try: read_file()
    except: file_exists = False

    # if the file exists, ask for confirmation
    if file_exists:
        answer = input('Vault already exists and you are about to reset it, erasing all of the stored data and passwords in the process. Proceed anyways? [y/n] ')
        if answer != 'y':
            print("Vault was not reset")
            return None
        else:
            print('Proceeding with Vault reset')

    #create file
    df = create_file()

    # setting master password
    master_pw = input_pw(timid=True)

    #encrypt file
    df = df_enc(df,master_pw)

    #create file from df
    override_file(df)

    return None


if __name__ == "__main__":
    unlockvault()
