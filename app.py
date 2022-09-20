import csv
import io
from sched import scheduler
from flask import Flask, jsonify, render_template, g, request
from database import Database
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from glissade import update_schema
from flask_json_schema import JsonValidationError, JsonSchema


app = Flask(__name__)
schema = JsonSchema(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({'error': e.message, 'errors': errors}), 400


# A2: Permet de rcuperer les donnees pendant l'execution du BackgroundSchedule
def job():
    with app.app_context():
        print('execution du BackgroundSchedule en cours...')
        get_db().get_data_from_requests()
        print("Fin d'exéxution du BackgroundSchedule")


scheduler = BackgroundScheduler(timezone='America/Montreal')
scheduler.add_job(job, 'cron', hour='0', minute=0)
scheduler.start()


# A3: affiche la documentation du REST API
@app.route('/doc')
def documentation():
    return render_template('doc.html')


# A4: retourner au format json les installations pour un arrondissement
@app.route('/api/installations')
def installations():
    if 'arrondissement' in request.args:
        arrondissement = request.args['arrondissement']
    else:
        return "Erreur: vous devez spécifier l'arrondissement", 404
    installations = get_db().get_installations(arrondissement)
    return jsonify(installations.informations())


# A5 et A6: la page d'acceuil avec le formulaire et la bare de recherche
@app.route('/', methods=['GET', 'POST'])
def acceuil():
    if request.method == 'GET':
        return render_template('acceuil.html')
    else:
        arrondissement = request.form['arrondissement']
        if arrondissement == '':
            return render_template('acceuil.html',
                                   error='Le champs ne '
                                   'peut pas être vide !')
        else:
            parametre = {'arrondissement': arrondissement}
            arr = requests.get('http://127.0.0.1:5000//api/installations',
                               params=parametre)
            arrondissements = arr.json()
            return render_template('installations.html',
                                   arrondissements=arrondissements)


# Pour A6: retourner au format json les informations sur une glissade
@app.route('/api/info-installation')
def info_installation():
    nom = request.args['nom']
    type = request.args['type']
    print(nom + ' ' + type)
    installation_info = get_db().get_info_installation(nom, type)
    if installation_info == 'vide':
        return 'Aucune information', 404
    else:
        if type == 'patinoire':
            return jsonify([patinoire.informations()
                            for patinoire in installation_info])
        else:
            return jsonify(installation_info.informations())


# Pour A6: afficher les informations sur une installation dans un template
@app.route('/installation/information')
def information_glissade():
    nom = request.args['nom']
    type = request.args['type']
    parametre = {'nom': nom, 'type': type}
    installation = requests.get('http://127.0.0.1:5000//api/info-installation',
                                params=parametre)
    info_installation = installation.json()
    if type == 'patinoire':
        return render_template('info_installation_patinoire.html',
                               all_patinoires=info_installation)
    else:
        return render_template('info_installation.html',
                               info_installations=info_installation)


# A6: retourner au format json toutes les installations avec leur type
@app.route('/api/all-installations')
def all_installations():
    all_installations = get_db().get_all_installations()
    return jsonify([installation.info() for installation in all_installations])


# Pour D1 et D2: retourner au format json une glissade si elle existe
@app.route('/api/une-glissade')
def gliss():
    if 'glissade' in request.args:
        glissade = request.args['glissade']
    else:
        return "Erreur: vous devez spécifier la glissade"
    gliss = get_db().get_glissade(glissade)
    if gliss is None:
        return 'aucune glissade', 404
    else:
        return jsonify(gliss.informations())


# D1: modifier une glissade
@app.route('/api/modifier-glissade', methods=['PUT'])
@schema.validate(update_schema)
def update_glissades():
    data = request.get_json()
    glissade = (data['nom_arr'], data['cle'], data['date_maj'],
                data['ouvert'], data['deblaye'], data['condition'],
                data['nom'])
    get_db().update_glisade(glissade)
    parametre = {'glissade': data['nom']}
    glissade_ = requests.get('http://127.0.0.1:5000//api/une-glissade',
                             params=parametre)
    if glissade_.status_code == 404:
        return 'aucune glissade', 404
    else:
        print(glissade_.status_code)
        glissade_ = glissade_.json()
        return (glissade_), 202


# D2: supprimer une glissade
@app.route('/api/supprimer-glissade', methods=['DELETE'])
def glissa():
    if 'glissade' in request.args:
        glissade = request.args['glissade']
    else:
        return "Erreur: vous devez spécifier la glissade"
    print(glissade)
    parametre = {'glissade': glissade}
    glissade_ = requests.get('http://127.0.0.1:5000//api/une-glissade',
                             params=parametre)
    if glissade_.status_code == 404:
        return 'aucune glissade', 404
    else:
        get_db().delete_glissade(glissade)
        return 'glissade supprimee', 200


# C1: recuperer toutes les informations au format json
@app.route('/api/type-installations_json')
def type_installations_json():
    type_installations = get_db().get_installation_types('json')
    installation_json = jsonify([installation.informations()
                                for installation in type_installations])
    # sorted(installation_json, key=lambda k: k['nom'], reverse=True)
    return installation_json


# C2: recuperer toutes les installations au format xml
@app.route('/api/type-installations_xml')
def type_installations_xml():
    type_installations = get_db().get_installation_types('xml')
    installation_xml = (type_installations.creer_xml())
    return installation_xml


# C3: recuperer toutes les installations au format csv
@app.route('/api/type-installations_csv')
def type_installations_csv():
    type_installations = get_db().get_installation_type_csv()
    collones = ['nom', 'nom_arr', 'type_installation']
    s_io = io.StringIO()
    ecrivin = csv.writer(s_io)
    ecrivin.writerow(collones)
    ecrivin.writerows(type_installations)
    content = s_io.getvalue()
    return content
