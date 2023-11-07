
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

        login = input("Input login credential for the password you want to get: ")

        self._decrypt_vault()

        pw = randomizer.random_sequence()

        try:
            self.vault[login] = pw
        except KeyError:
            self._encrypt_vault()
            print(f"Login '{login}' does not exist in the vault!")
            return

        self._insert_to_vault()

        pyperclip.copy(pw)
        print("\nChanged password copied to clipboard!")

        self._encrypt_vault()

    def new(self):
        """Updates `self.vault` dict and persists it into vault file."""

        login = input("Input login credential you want to add: ")

        self._decrypt_vault()

        try:
            if login in self.vault: raise KeyError
        except KeyError:
            self._encrypt_vault()
            print(f"Login '{login}' already exists in the vault.")
            return

        # Creating new password
        pw = randomizer.random_sequence()
        self.vault[login] = pw

        self._insert_to_vault()

        pyperclip.copy(pw)
        print("\nNew password copied to clipboard!")

        self._encrypt_vault()

    def get(self):
        """Looks up password corresponding to given login and copies it to clipboard."""

        login = input("Input login credential for the password you want: ")

        self._decrypt_vault()

        try:
            pw = self.vault[login]
        except KeyError:
            self._encrypt_vault()
            print(f"Login '{login}' not found in vault. Please check login list.")
            return

        pyperclip.copy(pw)
        print("\nPassword copied to clipboard!")

        self._encrypt_vault()

    def show(self):

        self._decrypt_vault()

        login_list = self.vault.keys()

        print("Printing list of saved login credentials:\n")
        for login in login_list:
            print(login)

        self._encrypt_vault()

if __name__ == "__main__":
    pass
