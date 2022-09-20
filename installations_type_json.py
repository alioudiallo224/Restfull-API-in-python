class Installation_type_json:
    def __init__(self, installation):
        self.installation = installation

    def informations(self):
        if self.installation[len(self.installation) - 1] == 'piscine':
            return {
                'id_uesv': self.installation[0],
                'type': self.installation[1],
                'nom': self.installation[2],
                'nom_arr': self.installation[3],
                'adresse': self.installation[4],
                'propriete': self.installation[5],
                'gestion': self.installation[6],
                'point_x': self.installation[7],
                'point_y': self.installation[8],
                'equipement': self.installation[9],
                'long': self.installation[10],
                'lat': self.installation[11],
                'type_installation': self.installation[12]
            }
        elif self.installation[len(self.installation) - 1] == 'glissade':
            return{
                'nom': self.installation[0],
                'nom_arr': self.installation[1],
                'cle': self.installation[2],
                'date_maj': self.installation[3],
                'ouvert': self.installation[4],
                'deblaye': self.installation[5],
                'condition': self.installation[6],
                'type_installation': self.installation[7]
            }
        elif self.installation[len(self.installation) - 1] == 'patinoire':
            return{
                'nom_arr': self.installation[0],
                'nom': self.installation[1],
                'type_installation': self.installation[2]
            }
