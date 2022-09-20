# Rapport
### Projet de session H2022
### Diallo, Mamadou Aliou
### DIAM02079904

## Liste des fonctionnalités devéloppée
- A1: Obtenir des trois listes de données et stocker leur contenu dans la base de données sql.
- A2: L'importation des données chaque jour à minuit.
- A3: La documentation des services REST.
- A4: Obtenir la liste des installations pour un arrondissement spécifié en paramètre.
- A5: La page d'acceuil avec un formulaire pour retourner les installations d'un arrondissement .
- A6: Une bare de recherche pur retourner les informations connues sur une installation recherchée.
- C1: Recupérer toutes les installations avec leur type au format json
- C2: Recupérer toutes les installations avec leur type au format xml
- C3: Recupérer toutes les installations avec leur type au format csv
- D1: Service Rest permettant de modifier une glissade
- D2: Service REST permettant de supprimer une glissade
- F1: Le système est entièrement déployé su la plateforme infonuagique Heroku
## Comment tester Les fonctionnalités:
### A1 et A2:
Pour tester, il faut changer l'horraire dans le backgroundSheduler. 
exemple: `'cron', hour='19', minute=9`

### A3:
Se rendre sur la route `/doc` et consulter les fichiers doc.raml qui est dans les dossiers statistics.

### A4:
Spécifier le nom de l'arrondissement en paramètre de la route: `/api/installations?arrondissement=<arrondissement>`.

### A5:
Se rendre sur la route `/`, entrer un arrondissement et soumettre.

### A6:
Se rendre sur la route `/`, choisir une installation à partir de la recherche et cliquer dessus pour afficher les informations.

### C1:
Entrer la route `/api/type-installations_json` dans postman.

### C2: 
Entrer la route `/api/type-installations_xml` dans postman.

### C3:
Entrer la route `/api/type-installations_csv` dans postman.

### D1:
Entrer la route `/api/modifier-glissade` dans postman. Entrer un format json valide exp: `{
    "nom" : "Aire de glissade, Ahuntsic",
    "nom_arr" : "Ahuntsic - Cartierville",
    "cle" : "ahc",
    "date_maj" : "2022-03-06 12:13:43",
    "ouvert" : 1,
    "deblaye" : 1,
    "condition" : "tres bonne"
}`

### D2: 
Entrer la route `/api/supprimer-glissade?glissade=<glisade>` dans postman en sp/cifiant la glissade à supprimer dans la route.

### F1:
`https://desolate-reef-62951.herokuapp.com/`.
