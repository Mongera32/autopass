# Importing required module
import subprocess
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
    login = getpass.getpass(prompt='Please input the desired login name: ', stream=None)
    return login

def decrypt_csv(key):
    try:
        subprocess.run(f'ccdecrypt --key {key} vault.csv', shell=True)
        return True
    except:
        print('File not found. Please check if it is encrypted and in the current directory')
        return False

def encrypt_csv(key):
    try:
        subprocess.run(f'ccencrypt --key {key} vault.csv', shell=True)
        return True
    except:
        print('File not found. Please check if it is decrypted and in the current directory')
        return False
