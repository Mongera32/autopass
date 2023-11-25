# What is this project?

This is a password vault that works locally. It manages your passwords and stores them in a file encrypted using AES (Advanced Encryption Standard). The main advantage of this is that all encrypted data is stored locally, therefore not relying on internet connection and eliminating risks associated with storing passwords in the cloud.

DISCLAIMER:
This is a personal project that is provided on an as is basis. No warranties of any kind, expressed or implied, are given.

# Installation

To install all requirements and the shell script shortcut for the project, go to the project root directory and input `bash ./sh-install.sh` in the shell. This command will install all dependencies and create a shell script so that you can use the functionalities of *autopass* anytime with a simple shell command.

# Usage

## Quickstart

The shell command to call autopass is `vault`. Type `vault add <SERVICE_NAME> -l` to begin using. <SERVICE_NAME> is the name of the site or service for which you want to store a password. **Example**: `vault add e-mail -l`

  - When you are using *autopass* for the firt time, this will prompt you to create a *master password*. Memorize this password and **DO NOT** forget it, otherwise you will **LOSE ACCESS** to all information stored with no way of getting it back.
  - Then, *autopass* will prompt you to insert your login id for your e-mail (e.g. myname@company.com)
  - Finally, *autopass* will generate a random strong password for this e-mail and store it in the encrypted file. It will be automatically transferred to your clipboard so it doesn't appear on your screen.

## Commands

`vault add <SERVICE_NAME> -l`: stores SERVICE_NAME, asks for a login id, generates a strong password and copies this password to clipboard.

`vault get <SERVICE_NAME>`: shows login id corresponding to SERVICE_NAME and copies it's password to clipboard.

`vault change <SERVICE_NAME>`: generates a new password for SERVICE_NAME and copies the new password to clipboard.


