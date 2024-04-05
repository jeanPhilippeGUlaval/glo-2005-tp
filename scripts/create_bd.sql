CREATE DATABASE dev;
USE dev;
CREATE TABLE users(id int PRIMARY KEY AUTO_INCREMENT, email varchar(256), password varchar(256));

-- CREATE TABLE log_table(log_line int PRIMARY KEY AUTO_INCREMENT, userID int, userEmail email varchar(256),  logTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, tokenExpires TIMESTAMP, FOREIGN KEY(userID) REFERENCES users(id), FOREIGN KEY(userEmail) REFERENCES users(email));

CREATE TABLE produits(ID_Produit INT AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE porte (ID int PRIMARY KEY, TAG varchar(70), Catégorie varchar(30), Largeur int, Hauteur int, isolation varchar(4), Motif int, Ferronerie varchar(24), Alliage varchar(24), Prix int, FOREIGN KEY (ID) REFERENCES produits(ID_Produit) ON DELETE CASCADE);
CREATE TABLE panneaux(ID int PRIMARY KEY, TAG varchar(70), Catégorie varchar(30), Largeur int, Hauteur int, isolation varchar(4), Modele varchar(255), Alliage varchar(24), Prix int, FOREIGN KEY (ID) REFERENCES produits(ID_Produit) ON DELETE CASCADE);
CREATE TABLE ferronnerie(ID int PRIMARY KEY, TAG varchar(70), Catégorie varchar(30), Largeur int, Hauteur int, Diametre varchar(6), Type varchar(24), Prix int, FOREIGN KEY (ID) REFERENCES produits(ID_Produit)ON DELETE CASCADE);

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

DELIMITER //
CREATE TRIGGER CalPrixTotalPorte
    BEFORE INSERT ON soumission_asso_porte
    FOR EACH ROW
    BEGIN
        SET NEW.sTotal = (SELECT SUM(p.prix * NEW.sQuantite) FROM porte p WHERE p.ID = NEW.ProductID);
    END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER CalPrixTotalFerronnerie
    BEFORE INSERT ON soumission_asso_ferronnerie
    FOR EACH ROW
    BEGIN
        SET NEW.sTotal = (SELECT SUM(p.prix * NEW.sQuantite) FROM ferronnerie f WHERE p.ID = NEW.ProductID);
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
  INSERT INTO produits VALUES (NULL);
  SET NEW.ID = LAST_INSERT_ID();
  SET NEW.TAG = 'PORTE DE GARAGE';
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER panneau_insert 
BEFORE INSERT ON panneaux 
FOR EACH ROW
BEGIN
  INSERT INTO produits VALUES (NULL);
  SET NEW.ID = LAST_INSERT_ID();
  SET NEW.TAG = 'PANNEAUX';
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER ferro_insert 
BEFORE INSERT ON ferronnerie 
FOR EACH ROW
BEGIN
  INSERT INTO produits VALUES (NULL);
  SET NEW.ID = LAST_INSERT_ID();
  SET NEW.TAG = 'FERRONNERIE';
END//
DELIMITER ;

