from flask import Flask, request, redirect
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)


@app.route("/run", methods=['POST'])
def output():
    return "Hello Michelle!"


@app.route('/receiver', methods=['POST'])
def worker():
    f = request.files['file']
    headers = None
    isNumeric = []
    with open("received_file.csv", "wb") as write_f:
        first = True
        second = False
        for line in f:
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