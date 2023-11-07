from plugins.vault_guard import VaultGuard
import logging

severity_level = logging.INFO
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(severity_level)

def main():

    print("""
    Select one of the following commands:

    1 - Get the password for a specific service.
    2 - Add credential to the vault.
    3 - Change the password for a specific service.
    4 - Show all saved services and respective logins (without passwords).
    5 - Delete a service credential from the vault.
    6 - Print a password in the screen.
    7 - Change master key
    """)

    cmd = int(input("Imput desired command number: "))

    if cmd == 1:
        guard = VaultGuard()
        guard.get()
        return

    if cmd == 2:
        guard = VaultGuard()
        guard.new()
        return

    if cmd == 3:
        guard = VaultGuard()
        guard.change()
        return

    if cmd == 4:
        guard = VaultGuard()
        guard.show()
        return

    if cmd == 5:
        guard = VaultGuard()
        guard.delete()
        return

    if cmd == 6:
        guard = VaultGuard()
        guard.show_password()
        return

    if cmd == 7:
        guard = VaultGuard()
        guard.change_master()
        return

    print("Command not recognized. Exiting program.")

if __name__ == "__main__":
    main()
