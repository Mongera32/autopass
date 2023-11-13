# What is this project?

This is a password vault that works locally. It manages your passwords and stores them in a file encrypted using AES (Advanced encryption standard). The main advantage of this is that all encrypted data is stored locally, therefore not relying on internet connection and eliminating risks associated with storing passwords in the cloud.

DISCLAIMER:
This is a personal project that is provided on an as is basis. no warranties or representations of any kind, expressed or implied, are given.

# Installation

To install all requirements and the shell script shortcut for the project, use the `bash ./sh-install.sh` in the project root directory.

# Usage

## Quickstart

The shell command to call autopass is `vault`. Type `vault add SERVICE_NAME -l` to begin using. SERVICE_NAME is the name of the site or service for which you want to store a password (e.g. e-mail).

When first calling the scrip, It will ask for a `master key` input. This the key that it will use for encrypting the file with sensitive data.
DO NOT forget this key, otherwise you will lose access to all stored data.
DO NOT write this key anywhere. This would pose security risks.

## Commands

`vault add SERVICE_NAME -l`: stores SERVICE_NAME, asks for a login id, generates a strong password and copies this password to clipboard.

`vault get SERVICE_NAME`: shows login id corresponding to SERVICE_NAME and copies it's password to clipboard.

`vault change SERVICE_NAME`: generates a new password for SERVICE_NAME and copies the new password to clipboard.


