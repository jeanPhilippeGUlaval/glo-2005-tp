CREATE DATABASE dev;
USE dev;
CREATE TABLE users(id int PRIMARY KEY AUTO_INCREMENT, email varchar(256), password varchar(256));

CREATE TABLE porte_id_gen(numerical_id INT AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE porte (ID VARCHAR(24) PRIMARY KEY, TAG varchar(70), Catégorie varchar(30), Largeur int, Hauteur int, isolation varchar(4), Motif int, Ferronerie varchar(24), Alliage varchar(24), Prix int);

CREATE TABLE panneaux_id_gen(numerical_id INT AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE panneaux(ID VARCHAR(24) PRIMARY KEY, TAG varchar(70), Catégorie varchar(30), Largeur int, Hauteur int, isolation varchar(4), Modele varchar(255), Alliage varchar(24), Prix int);

CREATE TABLE ferro_id_gen(numerical_id INT AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE ferronnerie(ID varchar(24) PRIMARY KEY, TAG varchar(70), Catégorie varchar(30), Largeur int, Hauteur int, Diametre varchar(6), Type varchar(24), prix int);

CREATE TABLE soumission_ids (ID VARCHAR(24) PRIMARY KEY, userID int, dateSoumission TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(userID) REFERENCES users(id) ON DELETE CASCADE);

CREATE TABLE soumission_asso_porte(sID VARCHAR(24),
ProductID VARCHAR(24) NOT NULL,
sQuantite int NOT NULL,
sTotal DECIMAL,
FOREIGN KEY (ProductID) REFERENCES porte(ID) ON DELETE CASCADE,
FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);

CREATE TABLE soumission_asso_panneaux(sID VARCHAR(24),
ProductID VARCHAR(24) NOT NULL,
sQuantite int NOT NULL,
sTotal DECIMAL,
FOREIGN KEY (ProductID) REFERENCES panneaux(ID) ON DELETE CASCADE,
FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);

CREATE TABLE soumission_asso_ferronnerie(sID VARCHAR(24),
ProductID VARCHAR(24) NOT NULL,
sQuantite int NOT NULL,
sTotal DECIMAL,
FOREIGN KEY (ProductID) REFERENCES ferronnerie(ID) ON DELETE CASCADE,
FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);


DELIMITER //
CREATE TRIGGER CalPrixTotalPanneau
    BEFORE INSERT ON soumission_asso_panneaux
    FOR EACH ROW
    BEGIN
        SET NEW.sTotal = (SELECT SUM(p.prix * NEW.sQuantite) FROM panneaux p WHERE p.ID = NEW.ProductID);
    END //
DELIMITER ;

-- DELIMITER //
-- CREATE TRIGGER NbCommandes
--     AFTER INSERT ON soumission
--     FOR EACH ROW
--     BEGIN
--        UPDATE porte
--        SET pQuantite = pQuantite + 1
--         WHERE porteId = NEW.porteId;

--     end //
-- DELIMITER ;


DELIMITER //
CREATE TRIGGER porte_insert 
BEFORE INSERT ON porte 
FOR EACH ROW
BEGIN
  INSERT INTO porte_id_gen VALUES (NULL);
  SET NEW.ID = CONCAT('PORTE-',(LAST_INSERT_ID()));
  SET NEW.TAG = 'PORTE DE GARAGE';
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER panneau_insert 
BEFORE INSERT ON panneaux 
FOR EACH ROW
BEGIN
  INSERT INTO panneaux_id_gen VALUES (NULL);
  SET NEW.ID = CONCAT('PANNE-',(LAST_INSERT_ID()));
  SET NEW.TAG = 'PANNEAUX';
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER ferro_insert 
BEFORE INSERT ON ferronnerie 
FOR EACH ROW
BEGIN
  INSERT INTO ferro_id_gen VALUES (NULL);
  SET NEW.ID = CONCAT('FERRO-',(LAST_INSERT_ID()));
  SET NEW.TAG = 'FERRONNERIE';
END//
DELIMITER ;

