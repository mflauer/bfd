import sqlite3
from sqlite3 import Error
import pandas as pd
 
# inputs user expects to query over
def make_db_for_user(original_csv, inputs: list):
    tableName = "test"
    # pull out only the columns relevant for their inputs
    original_df = pd.read_csv(original_csv)

    colInputs = inputs # the inputs that are directly names of columns
    colFilteredDf = original_df[colInputs]


    # go from our customized dataframe db file
    con = sqlite3.connect('{}.db'.format(tableName))
    with con:
        cur = con.cursor()
        colHeaders = ""
        for inp in inputs:
            if "numpy.float" in str(type(colFilteredDf.iloc[0][inp])):
                data_type = "FLOAT"
            else:
                data_type = "TEXT"
            colHeaders += ", " + inp + " " + data_type

        cur.execute("DROP TABLE {tablen}".format(tablen=tableName))
        cur.execute("CREATE TABLE {tablen}(id INTEGER PRIMARY KEY{headers})".format(tablen=tableName, headers=colHeaders))
        for index, row in colFilteredDf.iterrows():
            rowVal = str(index)
            for inp in inputs:
                current_val = row[inp]
                if "float" in str(type(current_val)):
                    if pd.isna(current_val):
                        current_val = 0
                    toAdd = str(current_val)
                else:
                    if pd.isna(current_val):
                        current_val = ""
                    toAdd = '"' + str(current_val) + '"'
                rowVal += "," + toAdd
            print("INSERT INTO {tablen} VALUES({val})".format(tablen=tableName, val=rowVal))
            cur.execute("INSERT INTO {tablen} VALUES({val})".format(tablen=tableName, val=rowVal))

    # return new db customized for them

def read_file():
    cnx = sqlite3.connect("test.db")
    df = pd.read_sql_query("SELECT * FROM test LIMIT 5", cnx)
    for ind, row in df.iterrows():
        print(row)

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
    make_db_for_user('movie_metadata.csv', ['director_name', 'duration'])
    read_file()