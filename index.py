from flask import Flask, render_template, request, redirect
# render_template -> indica il file html da visualizzare
# redirect -> la funzione di questo foglio python da eseguire
import os
from pymongo import MongoClient

def connect():
# Substitute the 5 pieces of information you got when creating
# the Mongo DB Database (underlined in red in the screenshots)
# Obviously, do not store your password as plaintext in practice
    connection = MongoClient("ds123933.mlab.com",23933)
    handle = connection["bebras"]
    handle.authenticate("annalisa","calcagni")
    return handle

app = Flask(__name__)
handle = connect()

# Bind our index page to both www.domain.com/ and www.domain.com/index
@app.route("/index" ,methods=['GET'])
@app.route("/", methods=['GET'])
def index():
    quesiti = [x for x in handle.tasks.find()]
    return render_template('index.html', quesiti=quesiti)

@app.route("/find", methods=['GET'])
def find():
    return render_template('cercauno.html')

# Remove the "debug=True" for production
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port, debug=True)