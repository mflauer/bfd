from flask import Flask, request, redirect
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/run")
def output():
    return "Hello Michelle!"

@app.route('/receiver', methods = ['POST'])
def worker():
    # read json + reply
    # print(request.get_json())
    # with open('testFile.txt', "wb") as file:
    #     file.write(request.form)
    f = request.files['file']
    print(f.read())
    return redirect("http://www.example.com")

if __name__ == "__main__":
    app.run("0.0.0.0", "5010")