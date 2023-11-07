
import os, subprocess, getpass, pyperclip, pickle
from . import randomizer
import logging
from colorama import Fore

severity_level = logging.INFO
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(severity_level)

class VaultGuard():

    # TODO implement test features
    def __init__(self) -> None:
        f"""
        Creates VaultGuard instance.

        `key` argument is the vault master key. Memorize this key and {Fore.RED}DO NOT FORGET IT{Fore.RESET},
        otherwise you will {Fore.RED}LOSE ACCESS TO YOUR VAULT{Fore.RESET}.
        """

        self._set_vault_path()

        if self._vault_check():
            self._vault_builder()

        self._input_master_key(confirm = False)

        self._access_vault()

    def _set_vault_path(self):
        """Sets path of vault.csv file"""

        path = os.path.dirname(os.path.realpath(__file__))
        logger.debug(f"path is {path}")
        #path = os.path.dirname(os.path.abspath(__file__))

        path_list = path.split("/")
        path_list.remove("plugins")
        path_list.append("vault")
        path = "/".join(path_list)

        self.decrypted_path = path
        self.encrypted_path = path + ".cpt"

        logger.debug(f"final path is {path}")

    def _vault_check(self) -> bool:
        """Returns True if vault does NOT exist and False otherwise."""

        if os.path.exists(self.encrypted_path) or os.path.exists(self.decrypted_path):
            return False

        return True

    def _input_master_key(self, confirm:bool = True):

        if hasattr(self,"key"):
            logger.debug("key has already been defined")
            return

        if confirm:

            key1 = getpass.getpass(prompt='\nPlease imput master key:', stream=None)
            key2 = getpass.getpass(prompt='\nPlease confirm master key: \n', stream=None)

            if key1 == key2:
                self.key = key1
            else:
                raise ValueError("Master key values don't match.")
            return

        self.key = getpass.getpass(prompt='\nPlease imput master key:', stream=None)

    def _vault_builder(self):
        """Builds and encrypts Vault"""

        confirmation = input(f"""
    {Fore.RED}WARNING{Fore.RESET}

    Vault will be built now and requires a user input master key to proceed.
    This key is needed to open your vault, and you will {Fore.RED}lose access{Fore.RESET} to all stored data in
    your vault if you forget the master key. proceed? [y/n]\n
""")
        if confirmation == "n":
            raise UserWarning("\nAborting\n")
        elif confirmation != 'y':
            raise UserWarning("\nCommand not recognized. Aborting.\n")
        elif confirmation == 'y':
            print("\nProceeding.\n")

        self._input_master_key(confirm = True)

        try:
            logger.debug("Building vault.")

            self.vault = {}

            with open(self.decrypted_path, "xb") as f:
                pickle.dump(self.vault, f)

            logger.debug("Vault building finished.")

        except FileExistsError:
            logger.debug(f"Vault already exists. Exiting vault builder.")

        self._encrypt_vault()

    def _decrypt_vault(self):

        if not self._check_encryption():
            logger.debug("Vault already decrypted")
            return

        logger.debug("Applying decryption")
        subprocess.run(f'ccdecrypt --key {self.key} {self.encrypted_path}', shell=True)
        logger.debug(f"Vault is now {Fore.RED}DECRYPTED{Fore.RESET}")

    def _encrypt_vault(self):

        if self._check_encryption():
            logger.debug("Vault already encrypted")
            return

        logger.debug("Applying encryption")
        subprocess.run(f'ccencrypt --key {self.key} {self.decrypted_path}', shell=True)
        logger.debug(f"Vault is now {Fore.GREEN}ENCRYPTED{Fore.RESET}")

    def _check_encryption(self) -> bool:
        """Returns True if encrypted and False if decrypted. Builds Vault and encrypts if it doesn't exist."""

        if os.path.exists(self.encrypted_path):
            return True

        if os.path.exists(self.decrypted_path):
            return False

        self._vault_builder()
        return True

    def _access_vault(self):
        """reads the vault file and unserializes the dict."""

        self._decrypt_vault()

        try:
            with open(self.decrypted_path,"rb") as f:
                vault = pickle.load(f)
                self.vault = vault
        except EOFError:
            self.vault = {}

        self._encrypt_vault()

    def _insert_to_vault(self):
        """Serializes ``self.vault`` dict into vault file."""

        with open(self.decrypted_path,"wb") as f:
            pickle.dump(self.vault,f)

    def change(self):

        service = input("Input login credential for the password you want to get: ")

        pw = randomizer.random_sequence()

        try:
            self.vault[service]["password"] = pw
        except KeyError:
            self._encrypt_vault()
            print(f"Service '{service}' does not exist in the vault!")
            return

        self._decrypt_vault()
        self._insert_to_vault()
        self._encrypt_vault()

        pyperclip.copy(pw)
        print("\nChanged password copied to clipboard!")

    def new(self):
        """Updates `self.vault` dict and persists it into vault file."""

        service = input("Input the name of the service you want to add: ")

        login = input("Input login credential you want to add: ")

        if login == "":
            login = service

        try:
            if service in self.vault: raise KeyError
        except KeyError:
            self._encrypt_vault()
            print(f"Data for '{service}' already exists in the vault.")
            return

        # Creating new password
        pw = randomizer.random_sequence()
        self.vault[service] = {"login":login,
                               "password":pw
        }

        self._decrypt_vault()
        self._insert_to_vault()
        self._encrypt_vault()

        pyperclip.copy(pw)
        print("\nNew password copied to clipboard!")

    def get(self):
        """Looks up password corresponding to given login and copies it to clipboard."""

        service = input("Input service name for the password you want: ")

        try:
            print(f"Login id : {Fore.BLUE + self.vault[service]['login'] + Fore.RESET}")
            pw = self.vault[service]["password"]
        except KeyError:
            self._encrypt_vault()
            print(f"Login for '{service}' not found in vault. Please check login list.")
            return

        pyperclip.copy(pw)
        print("\nPassword copied to clipboard!")

    def show(self):

        print("Printing list of saved login credentials:\n")
        for service in self.vault.keys():
            print(service + " -> " + self.vault[service]["login"])

    def delete(self):

        service1 = input("Input service credential for the password you want to delete: ")
        service2 = input(f"{Fore.RED}WARNING:{Fore.RESET} This cannot be undone. Input service again to confirm: ")

        if service1 == service2:
            service = service1
        else:
            raise ValueError("\nservice values don't match. Aborting.")

        try:
            self.vault.pop(service)
        except KeyError:
            print(f"service '{service}' does not exist in the vault. Aborting")

        self._decrypt_vault()
        self._insert_to_vault()
        self._encrypt_vault()

        print(f"\nservice {service} deleted!")

    def show_password(self):

        service = input("Input service name for the password you want: ")

        confirmation = input(f"{Fore.RED}WARNING:{Fore.RESET} you are about to show the password in your screen! proceed? [y/n]")

        if confirmation == "n":
            raise UserWarning("\nAborting\n")
        elif confirmation != 'y':
            raise UserWarning("\nCommand not recognized. Aborting.\n")
        elif confirmation == 'y':
            print("\nProceeding.\n")

        try:
            print(f"Login id : {Fore.BLUE + self.vault[service]['password'] + Fore.RESET}")
            pw = self.vault[service]["password"]
        except KeyError:
            self._encrypt_vault()
            print(f"Login for '{service}' not found in vault. Please check login list.")
            return

if __name__ == "__main__":
    pass
