import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np

# inputs user expects to query over
def make_db_for_user(original_csv, inputs: list):
    tableName = "test"
    # pull out only the columns relevant for their inputs
    original_df = pd.read_csv(original_csv)

    colInputs = []
    colInputs = list(inputs.keys()) # the inputs that are directly names of columns
    colFilteredDf = original_df[colInputs]

    # do more granular filtering (more specific than just column level)
    finalDf = colFilteredDf.copy()
    for inpKey in inputs:
        if inputs[inpKey] != None:
            # we have requested a particular column value
            finalDf = finalDf.loc[finalDf[inpKey] == inputs[inpKey]]

    # generate column headers for the db
    colHeaders = ""
    numericCols = {}
    for inp in inputs:
        isNumeric = np.issubdtype(type(finalDf.iloc[0][inp]),np.number)
        numericCols[inp] = isNumeric
        if isNumeric:
            data_type = "FLOAT"
        else:
            data_type = "TEXT"
        colHeaders += ", " + inp + " " + data_type

    # go from our customized dataframe db file
    con = sqlite3.connect('{}.db'.format(tableName))
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS {tablen}".format(tablen=tableName))
        cur.execute("CREATE TABLE {tablen}(id INTEGER PRIMARY KEY{headers})".format(tablen=tableName, headers=colHeaders))

        for index, row in finalDf.iterrows():
            rowVal = str(index)
            for colLabel in list(finalDf):
                currentVal = row[colLabel]
                if numericCols[colLabel]:
                    toAdd = str(currentVal) if not pd.isna(currentVal) else str(0)
                else:
                    toAdd = '"' + str(currentVal) + '"' if not pd.isna(currentVal) else '""'
                rowVal += "," + toAdd
            #print("INSERT INTO {tablen} VALUES({val})".format(tablen=tableName, val=rowVal))
            cur.execute("INSERT INTO {tablen} VALUES({val})".format(tablen=tableName, val=rowVal))

    # return new db customized for them

# used for testing purposes
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
    make_db_for_user('movie_metadata.csv', {'director_name': 'Peter Jackson', 'duration': None})
    read_file()
