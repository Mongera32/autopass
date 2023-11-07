
import os, subprocess, getpass, randomizer, pyperclip
import pandas as pd
import logging


severity_level = logging.DEBUG
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(severity_level)

class VaultGuard():

    def __init__(self, key) -> None:

        self.key = key
        self._set_vault_path()

        self._decrypt_csv()

        try:
            self._access_vault()
        except FileNotFoundError:
            self._vault_builder()
            self._access_vault()

        self._encrypt_csv()

    def _set_vault_path(self):
        """Sets path of vault.csv file"""

        path = os.path.dirname(os.path.abspath(__file__))

        path_list = path.split("/")
        path_list.remove("plugins")
        path_list.append("vault.csv")
        path = "/".join(path_list)

        self.decrypted_path = path
        self.encrypted_path = path + ".cpt"

    def _vault_check(self) -> bool:
        """Returns True e vault exists and False if not."""

        if os.path.exists(self.encrypted_path) or os.path.exists(self.decrypted_path):
            return True

        return False

    def _vault_builder(self):
        """Checks if vault exists and builds it if not."""

        if self._vault_check():
            return

        try:
            f = open(self.decrypted_path, "x")
            f.write("login password")
            f.close()
        except FileExistsError:
            f = open(self.decrypted_path, "w")
            f.truncate()
            f.write("login password")
            f.close()

    def _decrypt_csv(self):

        if not os.path.exists(self.encrypted_path) and os.path.exists(self.decrypted_path):
            print("Vault already decrypted")

        subprocess.run(f'ccdecrypt --key {self.key} {self.encrypted_path}', shell=True)

    def _encrypt_csv(self):

        if os.path.exists(self.encrypted_path) and not os.path.exists(self.decrypted_path):
            print("Vault already encrypted")

        subprocess.run(f'ccencrypt --key {self.key} {self.decrypted_path}', shell=True)

    def _access_vault(self):
        """reads the csv file and creates a DataFrame"""
        try:
            df = pd.read_csv(self.decrypted_path, sep = " ")
            if list(df.columns) != ["login","password"]:
                raise FileNotFoundError
        except (FileNotFoundError, pd.errors.EmptyDataError) as e:
            self._vault_builder()
            df = pd.read_csv(self.decrypted_path, sep = " ")

        self.df = df

    def get_login(self, login):
        """Looks up password corresponding to given login and copies it to clipboard."""

        filter = self.df['login'] == login
        row = self.df[filter]
        pw = row["password"][2]
        pyperclip.copy(pw)
        print("Password copied to clipboard!")

    def _check_for_duplicates(self, login) -> bool:
        """check if login appears on new dataframe more than once. Returns True if so."""

        filter = self.df['login'] == login
        if len(self.df[filter]) >= 1:
            return True
        return False

    def new_login(self, login):
        """Creates new dataframe row with the passed login and a random password"""

        self._decrypt_csv()

        if self._check_for_duplicates(login):
            raise KeyError("login already exists in vault")

        password = randomizer.random_sequence()

        new_row = pd.DataFrame({"login":[login],
                                "password":[password]
})

        df = pd.concat( [new_row, self.df],
                        axis = 0,
                        ignore_index = True)

        df.to_csv(  self.decrypted_path,
                    index = False,
                    sep = " ")

        pyperclip.copy(password)
        print("New password copied to clipboard!")

        self.df = df

        self._encrypt_csv()

    def change_login(self, login:str):

        self._decrypt_csv()

        password = randomizer.random_sequence()

        self.df.set_index("login")

        df = self.df

        df.loc[login,'password'] = password
        logger.debug(f"passwrod now: {password}")
        logger.debug(f"DataFrame now: {df}")

        df.reset_index()

        df.to_csv(  self.decrypted_path,
                    index = False,
                    sep = " ",)

        pyperclip.copy(password)
        print("Changed password copied to clipboard!")

        self._encrypt_csv()

if __name__ == "__main__":
    guard = VaultGuard("teste")
    guard.change_login("macaco2")

    guard._decrypt_csv()
