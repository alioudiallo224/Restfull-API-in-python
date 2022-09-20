import xml.etree.ElementTree as ET


class Installation_type_xml:
    def __init__(self, installations):
        self.installations = installations

    def creer_xml(self):
        root = ET.Element("Installations")
        for installation in self.installations:
            noeud_installation = ET.Element("installation")
            root.append(noeud_installation)
            if installation[len(installation) - 1] == 'piscine':
                id_uev = ET.SubElement(noeud_installation, "id_uev")
                id_uev.text = str(installation[0])
                type = ET.SubElement(noeud_installation, "type")
                type.text = str(installation[1])
                nom = ET.SubElement(noeud_installation, "nom")
                nom.text = str(installation[2])
                nom_arr = ET.SubElement(noeud_installation, "nom_arr")
                nom_arr.text = str(installation[3])
                adresse = ET.SubElement(noeud_installation, "adresse")
                adresse.text = str(installation[4])
                propriete = ET.SubElement(noeud_installation, "propriete")
                propriete.text = str(installation[5])
                gestion = ET.SubElement(noeud_installation, "gestion")
                gestion.text = str(installation[6])
                point_x = ET.SubElement(noeud_installation, "point_x")
                point_x.text = str(installation[7])
                point_y = ET.SubElement(noeud_installation, "point_y")
                point_y.text = str(installation[8])
                equipement = ET.SubElement(noeud_installation, "equipement")
                equipement.text = str(installation[9])
                long = ET.SubElement(noeud_installation, "long")
                long.text = str(installation[10])
                lat = ET.SubElement(noeud_installation, "lat")
                lat.text = str(installation[11])
                type_installation = ET.SubElement(noeud_installation,
                                                  "type_installation")
                type_installation.text = str(installation[12])
            elif installation[len(installation) - 1] == 'glissade':
                nom_g = ET.SubElement(noeud_installation, "nom")
                nom_g.text = str(installation[0])
                nom_arr_g = ET.SubElement(noeud_installation, "nom_arr")
                nom_arr_g.text = str(installation[1])
                cle = ET.SubElement(noeud_installation, "cle")
                cle.text = str(installation[2])
                date_maj = ET.SubElement(noeud_installation, "date_maj")
                date_maj.text = str(installation[3])
                ouvert = ET.SubElement(noeud_installation, "ouvert")
                ouvert.text = str(installation[4])
                deblaye = ET.SubElement(noeud_installation, "deblaye")
                deblaye.text = str(installation[5])
                condition = ET.SubElement(noeud_installation, "condition")
                condition.text = str(installation[6])
                type_installation = ET.SubElement(noeud_installation,
                                                  "type_installation")
                type_installation.text = str(installation[7])
            elif installation[len(installation) - 1] == 'patinoire':
                nom_p = ET.SubElement(noeud_installation, "nom")
                nom_p.text = str(installation[0])
                nom_arr_p = ET.SubElement(noeud_installation, "nom_arr")
                nom_arr_p.text = str(installation[1])
                type_installation = ET.SubElement(noeud_installation,
                                                  "type_installation")
                type_installation.text = str(installation[2])
        return ET.tostring(root)
