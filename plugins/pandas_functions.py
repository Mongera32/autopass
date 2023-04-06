import pandas as pd
from plugins.randomizer import random_sequence

def read_file():
    """reads the csv file and returns a dataframe"""
    return pd.read_csv('vault.csv', sep = " ")

def search_login(login):
    """returns row corresponding to given login"""

    df = read_file()
    filter = df['login'] == login
    row = df[filter]
    return row

def check_for_duplicates(login, df):
    """check if login appears on new dataframe more than once. Returns True if so."""

    filter = df['login'] == login
    if len(df[filter]) > 1:
        return True
    return False

def create_new_row(login,password):
    """Creates new dataframe row with the passed login and a random password"""

    new_row = pd.DataFrame(
                           [[login, password]],
                           columns=['login','password']
)
    return new_row

def pandas_concat(new_row):
    """Appends new row to original dataframe"""

    original_df = read_file()

    pd.concat([new_row, original_df], axis=0, ignore_index=True)
    return None
