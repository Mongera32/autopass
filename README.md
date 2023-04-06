# autopass
local cryptographed password vault. 

to use, call main(cmd), where cmd is a string with one of the following commands:

"encrypt" - encrypts the password vault (vault.csv).
"decrypt" - decrypts the password vault (vault.csv).
"addpw" - stores a login and password pair in the vault and sends password to clipboard.
"updatepw" - changes a password for passed login and sends password to clipboard.
"getpw" - fetches the password corresponding to the passed login and sends password to clipboard.
