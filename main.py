from plugins.data_manager import operation_manager, get_key, get_login, getpw, add_pw
from plugins.shell_interface import encrypt_csv, decrypt_csv

def main(cmd = 'getpw'):

    cmd = input("""
    Imput desired operation number:

    1 - get login
    2 - get password
    3 - insert login/password
    4 - encrypt
    5 - decrypt
          """)

    if cmd == 1:
        get_login()
        return

    if cmd == 2:
        getpw()
        return

    if cmd == 3:
        add_pw()
        return




if __name__ == "__main__":
    print("hello world!")

    # Check vault file

    # build vault if needed

    # ask for command


#    cmd = input('input command: ')
#    main(cmd)
