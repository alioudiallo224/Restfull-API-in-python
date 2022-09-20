class Patinoire:
    def __init__(self, patinoire):
        self.patinoire = patinoire

    def informations(self):
        return{
            'nom_pat': self.patinoire[0],
            'date_heures': self.patinoire[1],
            'ouvert': self.patinoire[2],
            'deblaye': self.patinoire[3],
            'arrose': self.patinoire[4],
            'resurface': self.patinoire[5]
        }
