# Importing required module
import subprocess
import getpass

def get_key():
    key = getpass.getpass(prompt='Encryption key: ', stream=None)
    return key

def get_login():
    login = getpass.getpass(prompt='login: ', stream=None)
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
