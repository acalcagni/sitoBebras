from flask import Flask, render_template, request, redirect, make_response
from pprint import pprint

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

@app.route("/elencoquesiti", methods=['GET'])
def elencoquesiti():
    type = request.args.get("type")
    id = request.args.get("id")

    if type=="ct":
        quesiti = handle.tasks.find({'computational_thinking':{'$in':[id]}})
    else:
        if type=="indicazioni":
            quesiti = handle.tasks.find({'indicazioni_nazionali':{'$in':[id]}})
        else:
            quesiti = handle.tasks.find()
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

@app.route("/traguardieobiettivi")
def traguardieobiettivi():
    result = request.args["id_quesito"]
    ind_task = handle.tasks.find_one({'id':result},{'_id':0,'indicazioni_nazionali':1})
    lista_id = ind_task.items()[0][1]
    indicazioninaz = handle.indicazioninazionali.find({'id_indicazioni':{'$in':lista_id}})
    j=0
    x=[]
    y=[]
    for i in indicazioninaz:
        #print i
        if i.items()[0][1]== "Matematica":
            y.append(i)
            print "ciao"
            print y
        x.append(i.items()[3][1])
    #print x
    return render_template('traguardieobiettivi.html', task=findTask(), x=x, y=y, indicazioninaz=indicazioninaz, indicazioni=True)


@app.route("/generaPdf", methods=['GET', 'POST'])
def generaPdf():
    getvalue = request.args
    titolo = getvalue["titolo"]
    data = request.form
    task = handle.tasks.find_one({'id':data.get("id_quesito")})
    rendered = render_template('pdftemplate.html', task = task, data=data, titolo=titolo)
    final=modify_img_path(rendered)
    file_class = Pdf()
    pdf = file_class.render_pdf(final)
    headers = {
        'content-type': 'application.pdf',
        'content-disposition': 'attachment; filename="%s_QuesitoBebras.pdf"' %(titolo)}
        #per fare il download automatico del PDF scrivere attachment
    return pdf, 200, headers

@app.route("/indicazioninazionali", methods=['GET'])
def indicazioninazionali():
    traguardi = handle.indicazioninazionali.find({'traguardo':{'$exists': True}})
    matematica_traguardi_elementari = handle.indicazioninazionali.find({'traguardo':{'$exists': True}, 'area_disciplinare': "Matematica", 'grado_scolastico': "Scuola primaria" }).sort('id_indicazioni',1)
    mat_ob_elem_terza_numeri = handle.indicazioninazionali.find({'obiettivo':{'$exists': True}, 'area_disciplinare': "Matematica", 'grado_scolastico': "Scuola primaria", 'classi_scolastiche' : "Fine classe terza", 'argomento_obiettivo' : "Numeri"}).sort('id_indicazioni',1)
    mat_ob_elem_terza_spazio = handle.indicazioninazionali.find({'obiettivo':{'$exists': True}, 'area_disciplinare': "Matematica", 'grado_scolastico': "Scuola primaria", 'classi_scolastiche' : "Fine classe terza", 'argomento_obiettivo' : "Spazio e figure"}).sort('id_indicazioni',1)
    mat_ob_elem_terza_relazioni = handle.indicazioninazionali.find({'obiettivo':{'$exists': True}, 'area_disciplinare': "Matematica", 'grado_scolastico': "Scuola primaria", 'classi_scolastiche' : "Fine classe terza", 'argomento_obiettivo' : "Relazioni, dati e previsioni"}).sort('id_indicazioni',1)
    mat_ob_elem_quinta_spazio = handle.indicazioninazionali.find({'obiettivo':{'$exists': True}, 'area_disciplinare': "Matematica", 'grado_scolastico': "Scuola primaria", 'classi_scolastiche' : "Fine classe quinta", 'argomento_obiettivo' : "Spazio e figure"}).sort('id_indicazioni',1)
    mat_ob_elem_quinta_relazioni = handle.indicazioninazionali.find({'obiettivo':{'$exists': True}, 'area_disciplinare': "Matematica", 'grado_scolastico': "Scuola primaria", 'classi_scolastiche' : "Fine classe quinta", 'argomento_obiettivo' : "Relazioni, dati e previsioni"}).sort('id_indicazioni',1)
    matematica_traguardi_medie = handle.indicazioninazionali.find({'traguardo':{'$exists': True}, 'area_disciplinare': "Matematica", 'grado_scolastico': "Scuola secondaria primo grado" }).sort('id_indicazioni',1)
    mat_ob_medie_numeri = handle.indicazioninazionali.find({'obiettivo':{'$exists': True}, 'area_disciplinare': "Matematica", 'grado_scolastico': "Scuola secondaria primo grado", 'argomento_obiettivo' : "Numeri"}).sort('id_indicazioni',1)
    mat_ob_medie_dati = handle.indicazioninazionali.find({'obiettivo':{'$exists': True}, 'area_disciplinare': "Matematica", 'grado_scolastico': "Scuola secondaria primo grado", 'argomento_obiettivo' : "Dati e previsioni"}).sort('id_indicazioni',1)
    scienze_traguardi_elementari = handle.indicazioninazionali.find({'traguardo':{'$exists': True}, 'area_disciplinare': "Scienze", 'grado_scolastico': "Scuola primaria" }).sort('id_indicazioni',1)
    tecnologia_ob_elem_vedere = handle.indicazioninazionali.find({'obiettivo':{'$exists': True}, 'area_disciplinare': "Tecnologia", 'grado_scolastico': "Scuola primaria", 'argomento_obiettivo' : "Vedere e osservare" }).sort('id_indicazioni',1)
    tecnologia_traguardi_med = handle.indicazioninazionali.find({'traguardo':{'$exists': True}, 'area_disciplinare': "Tecnologia", 'grado_scolastico': "Scuola secondaria primo grado"}).sort('id_indicazioni',1)
    tecnologia_ob_medie_prevedere = handle.indicazioninazionali.find({'obiettivo':{'$exists': True}, 'area_disciplinare': "Tecnologia", 'grado_scolastico': "Scuola secondaria primo grado", 'argomento_obiettivo' : "Prevedere, immaginare e progettare" }).sort('id_indicazioni',1)
    tecnologia_ob_medie_intervenire = handle.indicazioninazionali.find({'obiettivo':{'$exists': True}, 'area_disciplinare': "Tecnologia", 'grado_scolastico': "Scuola secondaria primo grado", 'argomento_obiettivo' : "Intervenire, trasformare e produrre" }).sort('id_indicazioni',1)
    return render_template('indicazioninazionali.html', traguardi=traguardi, matematica_traguardi_elementari=matematica_traguardi_elementari, mat_ob_elem_terza_numeri=mat_ob_elem_terza_numeri, mat_ob_elem_terza_spazio=mat_ob_elem_terza_spazio, mat_ob_elem_terza_relazioni=mat_ob_elem_terza_relazioni, mat_ob_elem_quinta_spazio=mat_ob_elem_quinta_spazio, mat_ob_elem_quinta_relazioni=mat_ob_elem_quinta_relazioni, matematica_traguardi_medie=matematica_traguardi_medie, mat_ob_medie_numeri=mat_ob_medie_numeri, mat_ob_medie_dati=mat_ob_medie_dati, scienze_traguardi_elementari=scienze_traguardi_elementari, tecnologia_ob_elem_vedere=tecnologia_ob_elem_vedere, tecnologia_traguardi_med=tecnologia_traguardi_med, tecnologia_ob_medie_prevedere=tecnologia_ob_medie_prevedere, tecnologia_ob_medie_intervenire=tecnologia_ob_medie_intervenire)

@app.route("/computationalthinking", methods=['GET'])
def computationalthinking():
    risultato = handle.computationalthinking.find().sort('id_ct',1)
    return render_template('computationalthinking.html', risultato=risultato)

def modify_img_path(imgpath):
    p = re.compile(r'/static/tasks/immagini/')
    return p.sub('/Users/annalisacalcagni/Documents/bebras/static/tasks/immagini/', imgpath)

def findTask():
    result = request.args["id_quesito"]
    task = handle.tasks.find_one({'id':result})
    return task


# Classe che crea il pdf dall'html
class Pdf():

    def render_pdf(self, html):

        from xhtml2pdf import pisa
        from StringIO import StringIO

        pdf = StringIO()

        pisa.CreatePDF(StringIO(html), pdf)

        return pdf.getvalue()

#def findIndicazioni():
 #   result = request.args["indicazioni_nazionali"]

  #  task = handle.indicazioninazionali.find({'id': })
   # return task

# Remove the "debug=True" for production
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    app.run(host='127.0.0.1', port=port, debug=True)


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
