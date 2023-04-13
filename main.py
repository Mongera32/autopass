from plugins.vault_manager import operation_manager
from plugins.encryption import encrypt_csv, decrypt_csv

def main(cmd = 'getpw'):

    operation_manager(cmd)

if __name__ == "__main__":
    cmd = input('input command: ')
    main(cmd)
