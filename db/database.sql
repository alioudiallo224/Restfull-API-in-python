CREATE TABLE piscines(
    id_uev          INTEGER,
    type_           VARCHAR,
    nom             VARCHAR,
    arrondissement  VARCHAR,
    adresse         VARCHAR,
    propriete       VARCHAR,
    gestion         VARCHAR,
    point_x         DECIMAL,
    point_y         DECIMAL,
    equipement      VARCHAR,
    long            DECIMAL,
    lat             DECIMAL
);

CREATE TABLE glissades(
    nom             VARCHAR,
    nom_arr         VARCHAR,
    cle             VARCHAR,
    deate_maj       DATE,
    ouvert          INTEGER,
    deblaye         INTEGER,
    condition       VARCHAR,
);

CREATE TABLE patinoires(
    nom_arr         VARCHAR,
    nom_pat         VARCHAR
)

CREATE TABLE conditions(
    nom_pat         VARCHAR,
    date_heure      VARCHAR,
    ouvert          INTEGER,
    deblaye         INTEGER,
    arrose          INTEGER,
    resurface       INTEGER
)