class Piscine:
    def __init__(self, id_uev, type, nom, arrondissement,
                 propriete, gestion, type_installation):
        self.id_uev = id_uev
        self.type = type
        self.nom = nom
        self.arrondissement = arrondissement
        self.propriete = propriete
        self.gestion = gestion
        self.type_installation = type_installation

    def informations(self):
        return {
            'id_uev': self.id_uev,
            'type': self.type,
            'nom': self.nom,
            'arrondissement': self.arrondissement,
            'propriete': self.propriete,
            'gestion': self.gestion
        }

    """def informations_type(self):
        return {
            'id_uev': self.id_uev,
            'type': self.type,
            'nom': self.nom,
            'arrondissement': self.arrondissement,
            'propriete': self.propriete,
            'gestion': self.gestion,
            'type_installation': self.type_installation
        }"""
