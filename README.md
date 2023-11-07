

# autopass

local cryptographed password vault.

To set it up, you must first call main with the "encrypt" command to encrypt the vault.

After that, call main and input the required data:

key: cryptographic key used to encrypt or decrypt the vault

login: login name that correspond to a password.

# installation:

Use the following command on shell to create autopass.sh file and move it to /usr/local/bin

MAINPATH=realpath main.py
LINE="python3 "
touch autopass.sh
echo $LINE > autopass.sh
echo echo $MAINPATH > autopass.sh
sudo mv autopass.sh /usr/local/bin

# commands

"encrypt" - encrypts the password vault (vault.csv).

"decrypt" - decrypts the password vault (vault.csv).

"addpw" - stores a login and password pair in the vault and sends password to clipboard.

"updatepw" - changes a password for passed login and sends password to clipboard.

"getpw" - fetches the password corresponding to the passed login and sends password to clipboard.
