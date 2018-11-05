from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/run")
def output():
    return "Hello Michelle!"

@app.route('/receiver', methods = ['POST'])
def worker():
    # read json + reply
    print(request.get_json())
    # with open('testFile.txt', "wb") as file:
    #     file.write(request.form)
    return "Hello"


if __name__ == "__main__":
    app.run("0.0.0.0", "5010")