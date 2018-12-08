from flask import Flask, request, redirect
from flask_cors import CORS
import json
from makedb import make_db_for_user, query_db, get_base_directory
from StructuredNLP import StructuredNLP
import os

app = Flask(__name__)
CORS(app)

S_NLP = None
FILENAMES = []
COLUMNS_NUMERIC = {}
JOIN_FIELDS = None
TABLENAME = None


@app.route("/reset_state", methods=['POST'])
def reset_state():
    global S_NLP, FILENAMES, COLUMNS_NUMERIC, JOIN_FIELDS, TABLENAME
    S_NLP = None
    FILENAMES = []
    COLUMNS_NUMERIC = {}
    JOIN_FIELDS = None
    TABLENAME = None
    return "State Reset"



@app.route("/run", methods=['POST'])
def output():
    return "Hello Michelle!"


@app.route('/file_saver', methods=['POST'])
def file_saver():
    global FILENAMES
    base_directory = get_base_directory()
    join = 2 == len(request.files.getlist("file"))
    for file in request.files.getlist("file"):
        fileLocation = "bfd_" + file.filename
        fileName = file.filename.split(".")[-2]
        FILENAMES.append((fileLocation, fileName))
        with open(os.path.join(base_directory, os.path.join("data_files", fileLocation)), "wb") as storedFile:
            lines = file.readlines()
            if join:
                first_line = lines[0]
                headers = first_line.decode().strip().split(",")
                rename_headers = map(lambda x: x + "_" + fileName, headers)
                joined_header = ",".join(rename_headers) + "\n"
                lines[0] = joined_header.encode()

            for line in lines:
                storedFile.write(line)

    if join:
        return "join.html"
    else:
        file_parser()
        return "columns.html"

@app.route('/table_name', methods=['POST'])
def table_name():
    global TABLENAME
    TABLENAME = list(request.form.keys())[0]
    return "Received table name"


@app.route('/file_parser', methods=['GET'])
def file_parser():
    global FILENAMES, COLUMNS_NUMERIC
    base_directory = get_base_directory()
    join_headers = {}

    for fileLocation, fileName in FILENAMES:
        isNumeric = []
        with open(os.path.join(base_directory, os.path.join("data_files", fileLocation)), "r") as read_f:
            headers = read_f.readline().strip().split(",")
            values = read_f.readline().strip().split(",")
            for val in values:
                if is_number(val):
                    isNumeric.append(True)
                else:
                    isNumeric.append(False)
        join_headers[fileName] = headers

        for index in range(len(headers)):
            COLUMNS_NUMERIC[headers[index]] = isNumeric[index]

    return json.dumps(join_headers)


@app.route("/get_column_numeric", methods=['GET'])
def get_column_numeric():
    global COLUMNS_NUMERIC
    return json.dumps(COLUMNS_NUMERIC)


@app.route("/receive_parameters_and_make_DB", methods=['POST'])
def receive_parameters_and_make_DB():
    global TABLENAME, FILENAMES, JOIN_FIELDS
    form_data = request.form
    parameter_dic = {}
    for key in form_data:
        value_list = form_data.getlist(key)
        value_list[0] = set(value_list[0].strip().split(", ")) if value_list[0] != "" else None
        value_list[1] = int(value_list[1]) if value_list[1] != "" else None
        value_list[2] = int(value_list[2]) if value_list[2] != "" else None
        parameter_dic[key[:-2]] = value_list

    result, isResultNumeric = make_db_for_user(FILENAMES, parameter_dic, TABLENAME, JOIN_FIELDS)
    global S_NLP
    if not result:
        return "Parameters received, no rows matched specifications, no bfd created"
    else:
        S_NLP = StructuredNLP(TABLENAME, result, isResultNumeric)
        return "Parameters received, bfd built"


@app.route("/join_values", methods=['POST'])
def join_values():
    global JOIN_FIELDS, COLUMNS_NUMERIC
    form_data = request.form
    j1 = form_data['j1']
    j2 = form_data['j2']

    JOIN_FIELDS = (j1, j2)
    del COLUMNS_NUMERIC[j2]
    return "Received merge parameters"


@app.route("/run_query", methods=['POST'])
def receive_query():
    global S_NLP
    output = json.dumps(S_NLP.runQuery())
    S_NLP.resetQuery()
    return output


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

@app.route("/reset_query", methods=['POST'])
def reset_query():
    global S_NLP
    return json.dumps(S_NLP.resetQuery())


@app.route("/get_options", methods=['POST'])
def get_options():
    sql_query = request.form['search_text']
    global S_NLP
    return json.dumps(S_NLP.updatePossibleSelections(sql_query))


# @app.route('/getpythondata')
# def get_python_data():
#     return json.dumps(pythondata)

if __name__ == "__main__":
    app.run("0.0.0.0", "5000")
