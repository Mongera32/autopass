from plugins.data_manager import operation_manager
from plugins.shell_interface import encrypt_csv, decrypt_csv

def main(cmd = 'getpw'):

    operation_manager(cmd)

if __name__ == "__main__":
    main()
