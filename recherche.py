class Recherche:
    def __init__(self, nom, cathegorie):
        self.nom = nom
        self.cathegorie = cathegorie

    def info(self):
        return {
            'installation': self.nom,
            'cathegorie': self.cathegorie
        }
