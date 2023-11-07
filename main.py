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

    1 - Get the password for a specific login.
    2 - Add a new login and password pair.
    3 - Change the password for a specific login.
    4 - Show all saved logins (without passwords).
    5 - Delete a login from the vault.
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

    print("No command select. Exiting program.")

if __name__ == "__main__":
    main()
