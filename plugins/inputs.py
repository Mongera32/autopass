import getpass

def input_login():
    """Asks user to imput their login"""
    service = input('Please input your login associated to the service (example: victor.silva@gmail.com): ')
    return service

def input_service():
    """Asks user to imput the service"""
    login = input(prompt='Please input the name of the service that want to save your password for (example: gmail,): ')
    return login

def input_pw(timid = True):
    """
    Asks user for a hidden "master password" imput and returns the password. \n
    Set "Timid = True" to ask user for a confirmation of the password.
    """

    # safe password imput
    password = getpass.getpass(prompt='Please input your master password: ', stream=None)

    # password confirmation if necessary
    if timid:
        confirmation = getpass.getpass(prompt='Please confirm your master password: ', stream=None)

        while password!=confirmation:
            password = getpass.getpass(prompt='Passwords do not match! Please input your master password again: ', stream=None)
            confirmation = getpass.getpass(prompt='Please confirm your master password again: ', stream=None)

    return password
