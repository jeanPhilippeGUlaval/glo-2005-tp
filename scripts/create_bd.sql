CREATE DATABASE dev;
USE dev;
CREATE TABLE users(id int PRIMARY KEY AUTO_INCREMENT, email varchar(256), password varchar(256));

CREATE TABLE porte_id_gen(numerical_id INT AUTO_INCREMENT PRIMARY KEY);

CREATE TABLE porte (ID VARCHAR(24) PRIMARY KEY, Description varchar(70), Catégorie varchar(30), Largeur int, Hauteur int, isolation varchar(4), Motif int, Ferronerie varchar(24), Alliage varchar(24), Prix int);

CREATE TABLE panneaux(ID VARCHAR(24) PRIMARY KEY, Description varchar(70), Catégorie varchar(30), Largeur int, Hauteur int, isolation varchar(4), Motif int, Ferronerie varchar(24), Alliage varchar(24), Prix int)

CREATE TABLE bundle_asso_color (bundleID int, colorId int, PRIMARY KEY (bundleID, colorId), FOREIGN KEY (bundleID) REFERENCES bundle(bundleID), FOREIGN KEY (colorId) REFERENCES color(colorId));

CREATE TABLE soumission_ids (ID VARCHAR(24) PRIMARY KEY);
-- CREATE TABLE soumission (ID VARCHAR(24), Produit VARCHAR(24),  Catégorie varchar(30), Prix int, FOREIGN KEY (ID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);

CREATE TABLE soumission_asso_porte(sID VARCHAR(24),
ProductID VARCHAR(24) NOT NULL,
sQuantite int NOT NULL,
sTotal DECIMAL,
dateSoumission TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (ProductID) REFERENCES porte(ID),
FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);

CREATE TABLE soumission_asso_panneaux(sID VARCHAR(24),
ProductID VARCHAR(24) NOT NULL,
sQuantite int NOT NULL,
sTotal DECIMAL,
dateSoumission TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (ProductID) REFERENCES panneaux(ID),
FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);

INSERT INTO soumission_ids Values ("testLocal");
INSERT INTO soumission_asso_panneaux (sID, ProductID, sQuantite) Values ("testLocal", "PANNE-1", 2);
INSERT INTO soumission_asso_porte (sID, ProductID, sQuantite) Values ("testLocal", "PORTE-1", 2);
DELETE FROM soumission_asso_panneaux WHERE sID = "testLocal";

DELIMITER //
CREATE TRIGGER CalPrixTotalPanneau
    BEFORE INSERT ON soumission_asso_panneaux
    FOR EACH ROW
    BEGIN
        SET NEW.sTotal = (SELECT SUM(p.prix * NEW.sQuantite) FROM panneaux p WHERE p.ID = NEW.ProductID);
    END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER NbCommandes
    AFTER INSERT ON soumission
    FOR EACH ROW
    BEGIN
       UPDATE porte
       SET pQuantite = pQuantite + 1
        WHERE porteId = NEW.porteId;

    end //
DELIMITER ;


SELECT * FROM soumission_asso_panneaux NATURAL RIGHT OUTER JOIN soumission_asso_porte; AS sp ON p.sID = sp.sID; WHERE sID = "testLocal";

SELECT ProductID FROM soumission_asso_panneaux UNION ALL SELECT ProductID FROM soumission_asso_porte WHERE sID = "testLocal";

SELECT Description FROM panneaux WHERE ID IN (SELECT ProductID FROM soumission_asso_panneaux UNION ALL SELECT ProductID FROM soumission_asso_porte WHERE sID = "testLocal");

DELIMITER //
CREATE TRIGGER porte_insert 
BEFORE INSERT ON porte 
FOR EACH ROW
BEGIN
  INSERT INTO porte_id_gen VALUES (NULL);
  SET NEW.ID = CONCAT('PORTE-',(LAST_INSERT_ID()));
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER porte_insert 
AFTER INSERT ON porte 
FOR EACH ROW
BEGIN
  SET NEW.ID = CONCAT('PORTE DE GARAGE',(LAST_INSERT_ID()));
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER porte_insert 
AFTER INSERT ON porte 
FOR EACH ROW
BEGIN
  SET NEW.ID = CONCAT('PANNEAUX DE PORTE DE GARAGE',(LAST_INSERT_ID()));
END//
DELIMITER ;


-- INSERT INTO soumission_ids VALUES ("Soumission_1");
-- INSERT INTO soumission VALUES ("Soumission_1", "PORTE-1","CABANON", 800);

-- DELETE FROM soumission_ids WHERE ID = 'Soumission_1';