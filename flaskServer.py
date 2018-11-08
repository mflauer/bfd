from flask import Flask, request, redirect
from flask_cors import CORS
import json
from makedb import make_db_for_user
app = Flask(__name__)
CORS(app)

current_file_name = "received_file.csv"


@app.route("/run", methods=['POST'])
def output():
    return "Hello Michelle!"


@app.route('/file_receiver', methods=['POST'])
def file_parser():
    f = request.files['file']
    headers = None
    isNumeric = []
    with open(current_file_name, "wb") as write_f:
        first = True
        second = False
        lines = f.readlines()
        for line in lines:
            if first:
                headers = line.decode().strip().split(",")
                first = False
                second = True
            elif second:
                values = line.decode().strip().split(",")
                for val in values:
                    if is_number(val):
                        isNumeric.append(True)
                    else:
                        isNumeric.append(False)
                second = False
            write_f.write(line)
    response = json.dumps([headers, isNumeric])
    return response


@app.route("/parameter_receiver", methods=['POST'])
def receive_parameters_and_make_DB():
    form_data = request.form
    parameter_dic = {}
    for key in form_data:
        value_list = form_data.getlist(key)
        value_list[0] = set(value_list[0].strip().split(", ")) if value_list[0] != "" else None
        value_list[1] = int(value_list[1]) if value_list[1] != "" else None
        value_list[2] = int(value_list[2]) if value_list[2] != "" else None
        parameter_dic[key[:-2]] = value_list

    result = make_db_for_user(current_file_name, parameter_dic, "received")
    if result:
        return "Parameters received, bfd built"
    else:
        return "Parameters received, no rows matched specifications, no bfd created"


@app.route("/receive_query", methods=['POST'])
def receive_query():
    print(request.form)
    return "Received Query"

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



# @app.route('/getpythondata')
# def get_python_data():
#     return json.dumps(pythondata)

if __name__ == "__main__":
    app.run("0.0.0.0", "5000")