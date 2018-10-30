import sqlite3
from sqlite3 import Error
import pandas as pd
 
# inputs user expects to query over
def make_db_for_user(original_csv, inputs: list):
    # pull out only the columns relevant for their inputs
    original_df = pd.read_csv(original_csv)

    colInputs = inputs # the inputs that are directly names of columns
    colFilteredDf = original_df[colInputs]

    # go from our customized dataframe db file
    


    # return new db customized for them


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
 
if __name__ == '__main__':
    #create_connection("C:\\sqlite\db\pythonsqlite.db")
    make_db_for_user('movie_metadata.csv', ['director_name'])