# autopass

local cryptographed password vault. 

To set it up, you must first call main with the "encrypt" command to encrypt the vault.

After that, call main(cmd), where cmd is a string with one of the following commands:

## commands:

"encrypt" - encrypts the password vault (vault.csv).

"decrypt" - decrypts the password vault (vault.csv).

"addpw" - stores a login and password pair in the vault and sends password to clipboard.

"updatepw" - changes a password for passed login and sends password to clipboard.

"getpw" - fetches the password corresponding to the passed login and sends password to clipboard.
