from plugins.vault_guard import VaultGuard
import logging, sys

severity_level = logging.INFO
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(severity_level)

def check_var(var):
    if not (var in locals()):
        raise NameError("Mandatory argument not defined.")

def main():

    args = sys.argv
    logger.debug(f"cmd: {args}")

    try:
        command = args[1]
    except IndexError:
        print("No command selected. Aborting.")
        return

    try:
        service = args[2]
    except IndexError:
        pass

    choose_password = False
    choose_login = False
    show_all = False

    if "-p" in args:
        choose_password = True
    if "-l" in args:
        choose_login = True
    if "-a" in args:
        show_all = True

    if command == 'help':

        print("""

        Arguments:

        get - Copy the password for a specific login to the clipboard.

        add - Add new credentials.

        change - Change the password for a specific login.

        show - Show all saved services and respective logins (does not show passwords).

        delete - Delete a credential from the vault.

        expose - Show a specific password on the screen.

        change_master - Changes your master key

        """)

        return

    try:
        check_var(service)
    except NameError:
        print("service not defined")

    if command == 'get':

        guard = VaultGuard()
        guard.get(service)
        return

    if command == 'add':

        guard = VaultGuard()
        guard.new(service,
                  choose_login=choose_login,
                  choose_password=choose_password)
        return

    if command == 'change':

        guard = VaultGuard()
        guard.change(service,
                     choose_password=choose_password)
        return

    if command == 'show':

        guard = VaultGuard()
        guard.show(service,
                   show_all=show_all)
        return

    if command == 'delete':

        guard = VaultGuard()
        guard.delete(service)
        return

    if command == 'expose':

        guard = VaultGuard()
        guard.expose(service)
        return

    if command == 'change_master':

        guard = VaultGuard()
        guard.change_master()
        return

    print("No command selected. Exiting program.")

if __name__ == "__main__":
    main()
