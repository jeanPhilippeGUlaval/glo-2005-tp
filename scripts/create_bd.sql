CREATE DATABASE dev;
USE dev;
CREATE TABLE users(id int PRIMARY KEY AUTO_INCREMENT, email varchar(256), password varchar(256));

CREATE TABLE produits(ID_Produit INT AUTO_INCREMENT PRIMARY KEY, produit VARCHAR(24));
CREATE TABLE porte (ID int PRIMARY KEY, TAG varchar(70), Catégorie varchar(30), Largeur int, Hauteur int, isolation varchar(4), Motif int, Ferronerie varchar(24), Alliage varchar(24), Prix int, FOREIGN KEY (ID) REFERENCES produits(ID_Produit) ON DELETE CASCADE);
CREATE TABLE panneaux(ID int PRIMARY KEY, TAG varchar(70), Catégorie varchar(30), Largeur int, Hauteur int, isolation varchar(4), Modele varchar(255), Alliage varchar(24), Prix int, FOREIGN KEY (ID) REFERENCES produits(ID_Produit) ON DELETE CASCADE);
CREATE TABLE ferronnerie(ID int PRIMARY KEY, TAG varchar(70), Catégorie varchar(30), Largeur int, Hauteur int, Diametre varchar(6), Type varchar(24), Prix int, FOREIGN KEY (ID) REFERENCES produits(ID_Produit)ON DELETE CASCADE);

CREATE TABLE soumission_ids (ID VARCHAR(24) PRIMARY KEY, userID int, dateSoumission TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(userID) REFERENCES users(id) ON DELETE CASCADE);

CREATE TABLE soumission_asso_porte(sID VARCHAR(24),
ProductID int NOT NULL,
sQuantite int NOT NULL,
sTotal DECIMAL,
FOREIGN KEY (ProductID) REFERENCES porte(ID) ON DELETE CASCADE,
FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);

CREATE TABLE soumission_asso_panneaux(sID VARCHAR(24),
ProductID int NOT NULL,
sQuantite int NOT NULL,
sTotal DECIMAL,
FOREIGN KEY (ProductID) REFERENCES panneaux(ID) ON DELETE CASCADE,
FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);

CREATE TABLE soumission_asso_ferronnerie(sID VARCHAR(24),
ProductID int NOT NULL,
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
        SET NEW.sTotal = (SELECT SUM(f.prix * NEW.sQuantite) FROM ferronnerie f WHERE f.ID = NEW.ProductID);
    END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AjouterSoumission(IN tableid varchar(50), IN produitID int, IN qty int,IN soumissionID varchar(24), IN productTable varchar(24))
BEGIN
    DECLARE total DECIMAL;    
    SET @sql := CONCAT("SELECT ProductID FROM ", tableid, " WHERE ProductID = ", produitID, " AND sID = '",soumissionID,"';");
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    IF FOUND_ROWS() > 0 THEN
        SET @sql := CONCAT("SELECT sQuantite into @tempQty FROM ", tableid, " WHERE ProductID = ", produitID, " AND sID = '",soumissionID,"';");
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SET @NewQty = qty + @tempQty;
        SET @sql := CONCAT("SELECT prix into @tempPrix FROM ", productTable, " WHERE ID = ", produitID,";");
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SET total = @NewQty * @tempPrix;
        
        SET @sql := CONCAT("UPDATE ", tableid, " SET sQuantite = ",@NewQty,", sTotal = ",total," WHERE ProductID = ",produitID, " AND sID ='",soumissionID,"';");
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    ELSE
        SET @sql := CONCAT("SELECT prix into @tempPrix FROM ", productTable, " WHERE ID = ", produitID,";");
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SET total = qty * @tempPrix;
        
        SET @sql := CONCAT("INSERT INTO ", tableid, " (sID, ProductID, sQuantite, sTotal) VALUES ('",soumissionID,"',",produitID,",",qty,",",total,");");
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END //
DELIMITER ;

SET @sql = CONCAT('SELECT prix FROM ', productTable, ' WHERE ID = ', produitID);
SET @sql = CONCAT('INSERT INTO 'tableid' (sID, ProductID, sQuantite, sTotal) VALUES (?,?,?);', soumissionID, produitID, qty, total);


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
  INSERT INTO produits (produit) VALUES ('porte');
  SET NEW.ID = LAST_INSERT_ID();
  SET NEW.TAG = 'PORTE DE GARAGE';
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER panneau_insert 
BEFORE INSERT ON panneaux 
FOR EACH ROW
BEGIN
  INSERT INTO produits (produit) VALUES ('panneaux');
  SET NEW.ID = LAST_INSERT_ID();
  SET NEW.TAG = 'PANNEAUX';
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER ferro_insert 
BEFORE INSERT ON ferronnerie 
FOR EACH ROW
BEGIN
  INSERT INTO produits (produit) VALUES ('ferronnerie');
  SET NEW.ID = LAST_INSERT_ID();
  SET NEW.TAG = 'FERRONNERIE';
END//
DELIMITER ;

