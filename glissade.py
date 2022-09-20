class Glissade:
    def __init__(self, nom, nom_arr, cle, date_maj, ouvert,
                 deblaye, condition, type_installation):
        self.nom = nom
        self.nom_arr = nom_arr
        self.cle = cle
        self.date_maj = date_maj
        self.ouvert = ouvert
        self.deblaye = deblaye
        self.condition = condition
        self.type_installation = type_installation

    def info(self):
        return {
            'nom': self.nom,
            'nom_arr': self.nom_arr,
            'cle': self.cle,
            'date_maj': self.date_maj
        }

    def informations(self):
        return {
            'nom': self.nom,
            'nom_arr': self.nom_arr,
            'cle': self.cle,
            'date_maj': self.date_maj,
            'ouvert': self.ouvert,
            'deblaye': self.deblaye,
            'condition': self.condition
        }

    def informations_type(self):
        return {
            'nom': self.nom,
            'nom_arr': self.nom_arr,
            'cle': self.cle,
            'date_maj': self.date_maj,
            'ouvert': self.ouvert,
            'deblaye': self.deblaye,
            'condition': self.condition,
            'type_installation': self.type_installation
        }


update_schema = {
    'type': 'object',
    'required': ['nom', 'nom_arr', 'cle', 'date_maj',
                 'ouvert', 'deblaye', 'condition'],
    'properties': {
        'nom': {
            'type': 'string'
        },
        'nom_arr': {
            'type': 'string'
        },
        'cle': {
            'type': 'string'
        },
        'date_maj': {
            'type': 'string'
        },
        'ouvert': {
            'type': 'number'
        },
        'deblaye': {
            'type': 'number'
        },
        'condition': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}
