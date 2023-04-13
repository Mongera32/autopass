import pandas as pd

def create_file():
    """Creates a vault.csv file in the correct format"""

    template = {'login':[], 'password':[]}

    df = pd.DataFrame(template)

    return df

def read_file():
    """reads the csv file and returns a dataframe"""
    return pd.read_csv('vault.csv', sep = " ")

def override_file(df:pd.DataFrame):
    df.to_csv(path_or_buf = 'vault.csv', index = False, sep = " ")
    return None

def search_index(login):
    """Identifies the index in a df corresponding to the passed login"""

    index = search_login(login).index[0]

    return index

def search_login(login):
    """returns row that contains the given login"""

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

def update_df(df:pd.DataFrame, index:int, login:str, password:str):
    """
    Inserts a row in a DataFrame or updates an existing row \n
    - index: \n
    Index of the row to be updated. Must be equal to the length of the DataFrame ( len(df) ) for this function to insert a new row. \n

    - login \n
    Login associated to the password \n

    - df \n
    Dataframe extracted from vault.csv \n

    - password \n
    Password to be inserted. \n
    """

    df.at[index,'login'] = login
    df.at[index,'password'] = password

    if check_for_duplicates(login,df):
        print('duplicate login found. Dataframe not updated')
        return None
    override_file(df)
    return None

if __name__ == "__main__":
    pass
