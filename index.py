from flask import Flask, render_template, request, redirect, make_response
from pprint import pprint
import pdfkit

# render_template -> indica il file html da visualizzare
# redirect -> la funzione di questo foglio python da eseguire
import os
import re
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
@app.route("/index", methods=['GET'])
@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/indicazioninazionali", methods=['GET'])
def indicazioninazionali():
    traguardi = handle.indicazioni.find({'traguardo':{'$exists': True}})
    return render_template('indicazioninazionali.html', traguardi=traguardi)

@app.route("/elencoquesiti", methods=['GET'])
def elencoquesiti():
    result = request.args
    quesiti = handle.tasks.find().sort([("titolo",1)])
    return render_template('elencoquesiti.html', quesiti=quesiti)

@app.route("/dettaglioquesito")
def dettaglioquesito():
    return render_template('dettaglioquesito.html', task=findTask(), testo=True)

@app.route("/soluzione")
def soluzione():
     return render_template('soluzione.html', task=findTask(), soluzione=True)

@app.route("/argomento_informatico")
def argomento_informatico():
     return render_template('argomento_informatico.html', task=findTask(), argomento=True)

@app.route("/generaPdf", methods=['POST'])
def generaPdf():
    data = request.form
    task = handle.tasks.find_one({'id':data.get("id_quesito")})
    rendered = render_template('pdftemplate.html', task = task)
    pdf = pdfkit.from_string(rendered, False)

    response= make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response


def findTask():
    result = request.args["id_quesito"]
    task = handle.tasks.find_one({'id':result})
    return task


# Remove the "debug=True" for production
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port, debug=True)


# Ricerca delle info sul task, ora rimpiazzato dallo script dataTables
#@app.route("/search", methods=['GET'])
#def search():
#    result = request.args
#    titolo = result["titolo"]
#    anno = result["anno"]
#    categoria = result["categoria"]
#    regx = re.compile(titolo, re.IGNORECASE)
#    annox = re.compile(anno)
#    categoriax = re.compile(categoria)
#    quesiti = handle.tasks.find({'titolo':{'$regex':regx},'anno':annox, 'categoria':categoriax}).sort([("titolo",1)])
#    return render_template('index.html', quesiti=quesiti)


#@app.route("/write", methods=['POST'])
#def write():
#    userinput = request.form.get("userinput")
#    risultato= handle.tasks.find({'titolo' : userinput})
#    return render_template ("cercauno.html", ris=risultato)
