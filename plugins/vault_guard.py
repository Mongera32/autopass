
import os, subprocess, getpass, pyperclip, pickle
from . import randomizer
import logging
from colorama import Fore
from prettytable import PrettyTable

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

    def _input_master_key(self, confirm:bool = True, override = False):

        if hasattr(self,"key") and not override:
            logger.debug("key has already been defined")
            return

        if confirm and not override:

            key1 = getpass.getpass(prompt='\nPlease input master key:', stream=None)
            key2 = getpass.getpass(prompt='\nPlease confirm master key: \n', stream=None)

            if key1 == key2:
                self.key = key1
            else:
                raise ValueError("Master key values don't match.")

        elif confirm and override:

            key1 = getpass.getpass(prompt='\nPlease input new master key:', stream=None)
            key2 = getpass.getpass(prompt='\nPlease confirm new master key: \n', stream=None)

            if key1 == key2:
                self.key = key1
            else:
                raise ValueError("Master key values don't match.")

        else:
            self.key = getpass.getpass(prompt='\nPlease input master key:', stream=None)

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

    def change(self, service:str, choose_password:bool = False):

        if choose_password:
            pw = getpass.getpass(prompt='\nPlease input desired password: ', stream=None)
        else:
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

    def new(self, service:str, choose_login:bool = False, choose_password:bool = False):
        """Updates `self.vault` dict and persists it into vault file."""

        if choose_login:
            login = input("Input login for the credential you want to add: ")
        else:
            login = service

        try:
            if service in self.vault: raise KeyError
        except KeyError:
            self._encrypt_vault()
            print(f"Data for '{service}' already exists in the vault.")
            return

        if choose_password:
            pw = getpass.getpass(prompt='\nPlease input desired password: ', stream=None)
        else:
            pw = randomizer.random_sequence()

        self.vault[service] = {"login":login,
                               "password":pw
        }

        self._decrypt_vault()
        self._insert_to_vault()
        self._encrypt_vault()

        pyperclip.copy(pw)
        print("\nNew password copied to clipboard!")

    def get(self, service:str):
        """Looks up password corresponding to given login and copies it to clipboard."""

        try:
            print(f"Login id : {Fore.BLUE + self.vault[service]['login'] + Fore.RESET}")
            pw = self.vault[service]["password"]
        except KeyError:
            self._encrypt_vault()
            print(f"Login for '{service}' not found in vault. Please check login list.")
            return

        pyperclip.copy(pw)
        print("\nPassword copied to clipboard!")

    def show(self, service, show_all = False):

        table = PrettyTable(["service","login"])

        if show_all:
            print("Printing credentials stored in the vault:\n")
            for key in self.vault.keys():
                table.add_row([key, self.vault[key]["login"]])
        else:
            print("Printing service and login:\n")
            table.add_row([service, self.vault[service]["login"]])

        print(table)

    def delete(self, service:str):

        if service not in self.vault:
            raise KeyError(f"service '{service}' does not exist in the vault. Aborting")

        print(f"""

        {Fore.RED}WARNING{Fore.RESET}

        You are about to delete your login and password for {Fore.BLUE + service + Fore.RESET}.

              """)

        confirmation = input("\nAre you absolutely sure you want to delete those credentials? [input service name in blue to continue]: ")

        if confirmation != service:
            print("\nInput does not match service name and confirmation failed. Aborting")
            return

        self.vault.pop(service)

        self._decrypt_vault()
        self._insert_to_vault()
        self._encrypt_vault()

        print(f"\nservice {service} deleted!")

    def expose(self, service:str):

        confirmation = input(f"{Fore.RED}WARNING:{Fore.RESET} you are about to show the login and password for {Fore.BLUE + service + Fore.RESET} in your screen! type {Fore.BLUE}y{Fore.RESET} to proceed: ")

        table = PrettyTable(["login","password"])

        if confirmation != "y":
            raise UserWarning("\nConfirmation failed. Aborting\n")

        try:
            table.add_row([self.vault[service]['login'],
                           self.vault[service]['password']])
            print(table)

        except KeyError:
            self._encrypt_vault()
            print(f"Login for '{service}' not found in vault. Please check login list.")
            return

    def change_master(self):

        confirmation = input(f"{Fore.RED}WARNING:{Fore.RESET} you are about to change the master key. Proceed? [y/n]")

        if confirmation == "n":
            raise UserWarning("\nAborting\n")
        elif confirmation != 'y':
            raise UserWarning("\nCommand not recognized. Aborting.\n")
        elif confirmation == 'y':
            print("\nProceeding.\n")

        self._decrypt_vault()

        try:
            self._input_master_key(confirm = True, override = True)
        except ValueError:
            self._encrypt_vault()
            return

        self._encrypt_vault()

if __name__ == "__main__":
    pass
