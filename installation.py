import json


class Instalation:
    def __init__(self, arrondissement, piscine, glissade, patinoire):
        self.arrondissement = arrondissement
        self.piscine = piscine
        self.glissade = glissade
        self.patinoire = patinoire

    def informations(self):
        return {
            'arrondissemen': self.arrondissement,
            'piscines': self.piscine,
            'glissades': self.glissade,
            'patinoires': self.patinoire
        }
