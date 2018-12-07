from flask import Flask, request, redirect
from flask_cors import CORS
import json
from makedb import make_db_for_user, query_db, get_base_directory
from StructuredNLP import StructuredNLP
import os

app = Flask(__name__)
CORS(app)

s = None
fileNames = []
columns_numeric = {}
join_fields = None
tableName = None


@app.route("/run", methods=['POST'])
def output():
    return "Hello Michelle!"


@app.route('/file_saver', methods=['POST'])
def file_saver():
    global fileNames
    base_directory = get_base_directory()
    join = 2 == len(request.files.getlist("file"))
    for file in request.files.getlist("file"):
        fileName = file.filename
        fileNames.append(fileName)
        with open(os.path.join(base_directory, os.path.join("data_files", file.filename)), "wb") as storedFile:
            lines = file.readlines()
            if join:
                first_line = lines[0]
                headers = first_line.decode().strip().split(",")
                rename_headers = map(lambda x: x + " (" + fileName + ")", headers)
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
    global tableName
    tableName = request.form
    return "Received table name"


@app.route('/file_parser', methods=['GET'])
def file_parser():
    global fileNames, columns_numeric
    base_directory = get_base_directory()
    join_headers = {}

    for file in fileNames:
        isNumeric = []
        with open(os.path.join(base_directory, os.path.join("data_files", file)), "r") as read_f:
            headers = read_f.readline().strip().split(",")
            values = read_f.readline().strip().split(",")
            for val in values:
                if is_number(val):
                    isNumeric.append(True)
                else:
                    isNumeric.append(False)
        join_headers[file] = headers

        print(headers)
        print(isNumeric)
        for index in range(len(headers)):
            columns_numeric[headers[index] + " (" + file + ")"] = isNumeric[index]

    return json.dumps(join_headers)


@app.route("/get_column_numeric", methods=['GET'])
def get_column_numeric():
    global columns_numeric
    return columns_numeric


@app.route("/parameter_receiver", methods=['POST'])
def receive_parameters_and_make_DB():
    global tableName, fileNames, join_fields
    form_data = request.form
    parameter_dic = {}
    for key in form_data:
        value_list = form_data.getlist(key)
        value_list[0] = set(value_list[0].strip().split(", ")) if value_list[0] != "" else None
        value_list[1] = int(value_list[1]) if value_list[1] != "" else None
        value_list[2] = int(value_list[2]) if value_list[2] != "" else None
        parameter_dic[key[:-2]] = value_list

    result, isResultNumeric = make_db_for_user(fileNames, parameter_dic, tableName, join_fields)
    global s
    if not result:
        return "Parameters received, no rows matched specifications, no bfd created"
    else:
        s = StructuredNLP(tableName, result, isResultNumeric)
        return "Parameters received, bfd built"


@app.route("/join_values", methods=['POST'])
def join_values():
    global join_fields, fileNames, columns_numeric
    form_data = request.form
    j1 = form_data['j1'] + " (" + fileNames[0] + ")"
    j2 = form_data['j2'] + " (" + fileNames[1] + ")"

    join_fields = (j1, j2)
    del columns_numeric[j2]
    return "Received merge parameters"


@app.route("/run_query", methods=['POST'])
def receive_query():
    global s
    output = json.dumps(s.runQuery())
    s.resetQuery()
    return output


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

@app.route("/reset_query", methods=['POST'])
def reset_query():
    global s
    return json.dumps(s.resetQuery())


@app.route("/get_options", methods=['POST'])
def get_options():
    sql_query = request.form['search_text']
    global s
    return json.dumps(s.updatePossibleSelections(sql_query))


# @app.route('/getpythondata')
# def get_python_data():
#     return json.dumps(pythondata)

if __name__ == "__main__":
    app.run("0.0.0.0", "5000")
