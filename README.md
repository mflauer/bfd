# bfd
## Setup
BFD was built with Python 3.7, although it should work with any version of Python 3. 

To set up, first run the command:
```pip install -r requirements.txt```

This will download and install flask.

## Running

To run locally, first start the flask server by running the command 
```python3 backend/flaskServer.py```

From here, simply open up a web browser and navigate to (preferably from Google Chrome)
http://localhost:63342/bfd/frontend/index.html

At this point simply upload the file you're interested in and follow the instructions that appear.


### Running non-locally
To run on a remote server, first start the remote server and 
change the last line of flaskServer.py from 
```app.run("0.0.0.0", "5000")``` to whatever the IP and port is of the machine
that you wish to run the server on. From there you must subsequently go into the .html files
in the frontend directory 
and change the ajax commands to communicate with your desired IP and port, rather than
with localhost. From there just start the server and open index.html and you should be 
good to go.
