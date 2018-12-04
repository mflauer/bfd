import sqlite3
import pandas as pd
import numpy as np
import os


# inputs user expects to query over
def make_db_for_user(original_csv: str, inputs: dict, table_name: str = "test"):
    # pull out only the columns relevant for their inputs
    original_df = pd.read_csv(original_csv)

    colInputs = list(inputs.keys()) # the inputs that are directly names of columns
    colFilteredDf = original_df[colInputs]

    # do more granular filtering (more specific than just column level)
    finalDf = colFilteredDf.copy()
    for inpKey in inputs:
        if inputs[inpKey][0] is not None:
            finalDf = finalDf.loc[finalDf[inpKey].isin(inputs[inpKey][0])]
        if inputs[inpKey][1] is not None:
            finalDf = finalDf.loc[finalDf[inpKey] > inputs[inpKey][1]]
        if inputs[inpKey][2] is not None:
            finalDf = finalDf.loc[finalDf[inpKey] < inputs[inpKey][2]]

    if finalDf.empty:
        print("No rows match, empty dataframe, no .db file created")
        return False

    # generate column headers for the db
    colIsNumeric = []
    colHeaders = ""
    numericCols = {}
    for inp in inputs:
        isNumeric = np.issubdtype(type(finalDf.iloc[0][inp]), np.number)
        numericCols[inp] = isNumeric
        if isNumeric:
            data_type = "FLOAT"
        else:
            data_type = "TEXT"
        colHeaders += ", '" + inp + "' " + data_type
        colIsNumeric.append(isNumeric)

    # go from our customized dataframe to db file

    directory = os.path.join(get_base_directory(), "data_files/")
    conn = sqlite3.connect(directory + table_name + ".db")
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS {tablen}".format(tablen=table_name))
        cur.execute("CREATE TABLE {tablen}(id INTEGER PRIMARY KEY{headers})".format(tablen=table_name, headers=colHeaders))

        for index, row in finalDf.iterrows():
            rowVal = str(index)
            for colLabel in list(finalDf):
                currentVal = row[colLabel]
                if numericCols[colLabel]:
                    toAdd = str(currentVal).lstrip().strip() if not pd.isna(currentVal) else str(0)
                else:
                    toAdd = '"' + str(currentVal).lstrip().strip() + '"' if not pd.isna(currentVal) else '""'
                rowVal += "," + toAdd
            cur.execute("INSERT INTO {tablen} VALUES({val})".format(tablen=table_name, val=rowVal))

    # return new db customized for them
    return colInputs, colIsNumeric


def query_db(sql_query, table_name):
    directory = os.path.join(get_base_directory(), "data_files/")
    conn = sqlite3.connect(directory + table_name + ".db")
    cur = conn.cursor()
    results = cur.execute(sql_query).fetchall()
    return results


# used for testing purposes
def read_file(table_name):
    directory = os.path.join(get_base_directory(), "data_files/")
    conn = sqlite3.connect(directory + table_name + ".db")
    df = pd.read_sql_query("SELECT * FROM {} LIMIT 10".format(table_name), conn)
    for ind, row in df.iterrows():
        print(row)


def get_base_directory():
    current_directory = os.getcwd()
    path = ("", current_directory)
    while path[1] != "bfd":
        path = os.path.split(current_directory)
        current_directory = path[0]
    return os.path.join(path[0], path[1])

 
if __name__ == '__main__':
    # make_db_for_user('movie_metadata.csv', {'director_name': {'Christopher Nolan', 'James Cameron'}, 'duration': [100, 120], 'movie_title': None})
    print(query_db("SELECT director_name FROM BFD limit 50;", "BFD"))

