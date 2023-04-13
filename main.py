from plugins.vault_manager import operation_manager
from plugins.encryption import encrypt_csv, decrypt_csv

def main(cmd = 'getpw'):

    # check if vault.csv exists
    # create vault.csv if it doesnt't exist
    pass

if __name__ == "__main__":
    cmd = input('input command: ')
    main(cmd)
