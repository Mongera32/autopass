# Importing required module
import subprocess
# import required module
from cryptography.fernet import Fernet
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

def encryptFile(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_file:
            Input file

        out_file:
            If None, a StringIO will be returned.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def encrypt_csv(key):
    try:
        subprocess.run(f'ccencrypt --key {key} vault.csv', shell=True)
        return True
    except:
        print('File not found. Please check if it is decrypted and in the current directory')
        return False

ferencrypt('nhf8923hf89233f2io')