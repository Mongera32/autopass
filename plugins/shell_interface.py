# Importing required module
import subprocess
# import required module
import bcrypt
import getpass

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