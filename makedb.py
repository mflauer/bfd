import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np

# inputs user expects to query over
def make_db_for_user(original_csv: str, inputs: dict):
    tableName = "test"
    # pull out only the columns relevant for their inputs
    original_df = pd.read_csv(original_csv)

    colInputs = list(inputs.keys()) # the inputs that are directly names of columns
    colFilteredDf = original_df[colInputs]

    # do more granular filtering (more specific than just column level)
    finalDf = colFilteredDf.copy()
    for inpKey in inputs:
        if inputs[inpKey] is None:
            continue
        elif type(inputs[inpKey]) == str:
            # we have requested a particular column value
            finalDf = finalDf.loc[finalDf[inpKey] == inputs[inpKey]]
        elif type(inputs[inpKey]) == set:
            # we have requested multiple values from column
            finalDf = finalDf.loc[finalDf[inpKey].isin(inputs[inpKey])]
        elif type(inputs[inpKey]) == list:
            # We have requested range of values
            finalDf = finalDf.loc[(finalDf[inpKey] > inputs[inpKey][0]) & (finalDf[inpKey] < inputs[inpKey][1])]

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

    # go from our customized dataframe to db file
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
            cur.execute("INSERT INTO {tablen} VALUES({val})".format(tablen=tableName, val=rowVal))

    # return new db customized for them

# used for testing purposes
def read_file():
    cnx = sqlite3.connect("test.db")
    df = pd.read_sql_query("SELECT movie_title FROM test LIMIT 5", cnx)
    for ind, row in df.iterrows():
        print(row)

 
if __name__ == '__main__':
    make_db_for_user('movie_metadata.csv', {'director_name': {'Christopher Nolan', 'James Cameron'}, 'duration': [100, 120], 'movie_title': None})
    read_file()

