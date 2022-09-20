import sqlite3
import pandas as pd
import urllib.request
import xml.etree.ElementTree as et
from installations_type_json import Installation_type_json
from installations_type_xml import Installation_type_xml
from installation import Instalation
from recherche import Recherche
from patinoire import Patinoire
from glissade import Glissade
from piscine import Piscine


class Database():

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    # Recuperer des données des piscines en csv puis les stocker
    # dans la table piscines
    def donnees_piscines(self):
        colonnes_piscines = ['id_uev', 'type', 'nom', 'nom_arr', 'adresse',
                             'propriete', 'gestion', 'point_x', 'point_y',
                             'equipement', 'long', 'lat']
        piscines = pd.read_csv('https://data.montreal.ca/dataset/4604afb7-a7'
                               'c4-4626-a3ca-e136158133f2/resource/cbdca706-'
                               '569e-4b4a-805d-9af73af03b14/download/piscin'
                               'es.csv',
                               names=colonnes_piscines, header=None,
                               skiprows=[0])
        piscines.sort_values(by=['nom'])
        piscines.to_sql('piscines', self.get_connection(),
                        if_exists='replace', index=False)

    # Recuperer les données des glissades en xml puis les stocker
    # dans la table glissade
    def donnees_glissades(self):
        with urllib.request.urlopen('http://www2.ville.montreal.qc.ca/'
                                    'services_citoyens/pdf_transfert/'
                                    'L29_GLISSADE.xml') as url:
            donnes_xml_glissades = et.parse(url)
            glissades_ = donnes_xml_glissades.getroot()
            colonnes = ['nom', 'nom_arr', 'cle', 'date_maj',
                        'ouvert', 'deblaye', 'condition']
            lignes = []
            for glissade in glissades_:
                nom_ = glissade.find('nom').text
                nom_arr_ = glissade.find('arrondissement').find('nom_arr').text
                cle_ = glissade.find('arrondissement').find('cle').text
                date_maj_ = glissade.find('arrondissement'
                                          ).find('date_maj').text
                ouvert_ = glissade.find('ouvert').text
                deblaye_ = glissade.find('deblaye').text
                condition_ = glissade.find('condition').text

                nom_arr_ = " ".join(nom_arr_.split()).replace(" - ", "-")
                nom_ = " ".join(nom_.split()).replace(" - ", "-")

                lignes.append({'nom': (nom_), 'nom_arr': nom_arr_, 'cle': cle_,
                               'date_maj': date_maj_, 'ouvert': ouvert_,
                               'deblaye': deblaye_, 'condition': condition_})
            glissades = pd.DataFrame(lignes, columns=colonnes)
            glissades.sort_values(by=['nom'])
            glissades.to_sql('glissades', self.get_connection(),
                             if_exists='replace', index=False)

    # Recuperer les données des patinoires en xml puis les stocker dans
    # deux tables distinctes.
    # table patinoires: contient les noms des patinoires et les arrondissemnts
    # table conditions: contient le nom d'une patinoire et les données des
    # conditions de différentes dates qui sont liées à cette patinoire
    def donnees_patinoires(self):
        with urllib.request.urlopen('https://data.montreal.ca/dataset/'
                                    '225ac315-49fe-476f-95bd-a1ce1648a98c/'
                                    'resource/5d1859cc-2060-4def-903f-db24408'
                                    'bacd0/download/l29-patinoire.xml') as url:
            donnees_xml_patinoires = et.parse(url)
            patinoires_ = donnees_xml_patinoires.getroot()
            colonnes_patinoires_ = ['nom_arr', 'nom_pat']
            collones_conditions_ = ['nom_pat', 'date_heure', 'ouvert',
                                    'deblaye', 'arrose', 'resurface']
            lignes = []
            lignes_conditions = []
            for patinoire in patinoires_:
                nom_arr_ = patinoire.find('nom_arr').text
                nom_pat_ = patinoire.find('patinoire').find('nom_pat').text
                nom_arr_ = " ".join(nom_arr_.split()).replace(" - ", "-")
                nom_pat_ = " ".join(nom_pat_.split()).replace(" - ", "-")
                for condition in patinoire.find('patinoire'
                                                ).findall('condition'):
                    date_heure_ = condition.find('date_heure').text
                    ouvert_ = condition.find('ouvert').text
                    deblaye_ = condition.find('deblaye').text
                    arrose_ = condition.find('arrose').text
                    resurface_ = condition.find('resurface').text

                    lignes_conditions.append({'nom_pat': nom_pat_,
                                              'date_heure': date_heure_,
                                              'ouvert': ouvert_,
                                              'deblaye': deblaye_,
                                              'arrose': arrose_,
                                              'resurface': resurface_})
                lignes.append({'nom_arr': nom_arr_, 'nom_pat': nom_pat_})
            patinoires = pd.DataFrame(lignes, columns=colonnes_patinoires_)
            conditions = pd.DataFrame(lignes_conditions,
                                      columns=collones_conditions_)
            patinoires.sort_values(by=['nom_pat'])
            patinoires.to_sql('patinoires', self.get_connection(),
                              if_exists='replace', index=False)
            conditions.to_sql('conditions', self.get_connection(),
                              if_exists='replace', index=False)

    # Ajouter une colonne type_installation à la table piscines
    def add_type_piscines(self):
        cursor = self.get_connection()
        cursor.execute('ALTER TABLE piscines ADD COLUMN '
                       'type_installation DEFAULT "piscine" ')
        cursor.commit()

    # Ajouter une colonne type_installation à la table glissades
    def add_type_glissades(self):
        cursor = self.get_connection()
        cursor.execute('ALTER TABLE glissades ADD COLUMN '
                       'type_installation DEFAULT "glissade" ')
        cursor.commit()

    # Ajouter une colonne type_installation à la table patinoires
    def add_type_patinoires(self):
        cursor = self.get_connection()
        cursor.execute('ALTER TABLE patinoires ADD COLUMN '
                       'type_installation DEFAULT "patinoire" ')
        cursor.commit()

    # Stocker les données dans la base de données avec la colonne
    # type_installation en utilisant les fonctions précedentes
    def get_data_from_requests(self):
        self.donnees_piscines()
        self.add_type_piscines()
        self.donnees_glissades()
        self.add_type_glissades()
        self.donnees_patinoires()
        self.add_type_patinoires()

    # Retourner l'ensemble des installations d'un arrondissement
    def get_installations(self, arrondissement):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT nom FROM glissades WHERE nom_arr=?',
                       (arrondissement,))
        glissades = cursor.fetchall()
        cursor.execute('SELECT nom_pat FROM patinoires WHERE nom_arr=?',
                       (arrondissement,))
        patinoires = cursor.fetchall()
        cursor.execute('SELECT nom FROM piscines WHERE nom_arr=?',
                       (arrondissement,))
        piscines = cursor.fetchall()
        return (Instalation(arrondissement, piscines, glissades, patinoires))

    # Retourner toutes les glissades
    def get_glissades(self):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT * FROM glissades')
        glissades = cursor.fetchall()
        return (Glissade(glissade[0], glissade[1], glissade[2],
                         glissade[3], glissade[4], glissade[5],
                         glissade[6], [glissade[7]])
                for glissade in glissades)

    # Retourner toutes les installations de type glissade, piscine et patinoire
    def get_all_installations(self):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT nom, type_installation FROM glissades')
        glissades = cursor.fetchall()
        cursor.execute('SELECT nom_pat, type_installation FROM patinoires')
        patinoires = cursor.fetchall()
        cursor.execute('SELECT nom, type_installation FROM piscines')
        piscines = cursor.fetchall()
        installations = glissades + patinoires + piscines
        return (Recherche(installation[0], installation[1])
                for installation in installations)

    # Retouner une glissade qui correspond à un nom donné
    def get_glissade(self, nom):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT * FROM glissades WHERE nom=?', (nom,))
        glissade = cursor.fetchone()
        if glissade is None:
            return None
        else:
            return (Glissade(glissade[0], glissade[1], glissade[2],
                             glissade[3], glissade[4], glissade[5],
                             glissade[6], glissade[7]))

    # Supprimer une glissade qui correspond à un nom donné
    def delete_glissade(self, nom):
        cursor = self.get_connection()
        cursor.execute('DELETE FROM glissades WHERE nom=?', (nom,))
        cursor.commit()

    # Mettre à jour une glissade
    def update_glisade(self, glissade):
        cursor = self.get_connection()
        sql_request = '''UPDATE glissades
                          SET nom_arr = ? ,
                              cle = ? ,
                              date_maj = ? ,
                              ouvert = ? ,
                              deblaye = ? ,
                              condition = ?
                          WHERE nom = ?'''
        cursor.execute(sql_request, (glissade))
        print()
        cursor.commit()

    # Rtourner toutes les informations connues sur une glissade,
    # une piscine ou une patinoire qui correspond au nom donné
    def get_info_installation(self, nom, type):
        cursor = self.get_connection().cursor()
        if type == 'piscine':
            cursor.execute('SELECT * FROM piscines WHERE nom=?', (nom,))
            piscines = cursor.fetchone()
            if piscines is None:
                return 'aucune piscine'
            else:
                return (Piscine(piscines[0], piscines[1], piscines[2],
                                piscines[4], piscines[5], piscines[6],
                                piscines[7]))
        elif type == 'glissade':
            cursor.execute('SELECT * FROM glissades WHERE nom=?', (nom,))
            glissades = cursor.fetchone()
            if glissades is None:
                return 'aucune glissade'
            else:
                return (Glissade(glissades[0], glissades[1], glissades[2],
                                 glissades[3], glissades[4], glissades[5],
                                 glissades[6], glissades[7]))
        elif type == 'patinoire':
            cursor.execute('SELECT * FROM conditions WHERE nom_pat=?', (nom,))
            patinoires = cursor.fetchall()
            if patinoires is None:
                return 'aucune patinoire'
            else:
                return (Patinoire(patinoire) for patinoire in patinoires)

    # Retourne toutes les installations avec le bon format choisi
    # en fonction du type(json et xml)
    def get_installation_types(self, type):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT * FROM glissades')
        glissades = cursor.fetchall()
        cursor.execute('SELECT * FROM patinoires')
        patinoires = cursor.fetchall()
        cursor.execute('SELECT * FROM piscines')
        piscines = cursor.fetchall()
        inst = glissades + patinoires
        installations = piscines + inst
        if type == 'json':
            return (Installation_type_json(installation)
                    for installation in installations)
        elif type == 'xml':
            return (Installation_type_xml(installations))

    # Retourne les installations au format csv
    def get_installation_type_csv(self):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT nom, nom_arr, type_installation FROM glissades')
        glissades = cursor.fetchall()
        cursor.execute('SELECT nom_pat, nom_arr, '
                       'type_installation FROM patinoires')
        patinoires = cursor.fetchall()
        cursor.execute('SELECT nom, nom_arr, type_installation FROM piscines')
        piscines = cursor.fetchall()
        inst = glissades + patinoires
        installations = piscines + inst
        return (installations)
