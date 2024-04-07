CREATE DATABASE dev;
USE dev;
CREATE TABLE users(ID int PRIMARY KEY AUTO_INCREMENT, email varchar(256), password varchar(256));

CREATE TABLE produits(ID INT AUTO_INCREMENT PRIMARY KEY, TAG VARCHAR(70), Catégorie varchar(30), prix int);
CREATE TABLE porte (ID int, Largeur int, Hauteur int, isolation varchar(4), Motif int, Ferronerie varchar(24), Alliage varchar(24), FOREIGN KEY (ID) REFERENCES produits(ID) ON DELETE CASCADE);
CREATE TABLE panneaux(ID int, Largeur int, Hauteur int, isolation varchar(4), Modele varchar(255), Alliage varchar(24), FOREIGN KEY (ID) REFERENCES produits(ID) ON DELETE CASCADE);
CREATE TABLE ferronnerie(ID int, Largeur int, Hauteur int, Diametre varchar(6), Type varchar(24), FOREIGN KEY (ID) REFERENCES produits(ID) ON DELETE CASCADE);

CREATE TABLE soumission_ids (ID VARCHAR(24) PRIMARY KEY, userID int, dateSoumission TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(userID) REFERENCES users(ID) ON DELETE CASCADE);

CREATE TABLE soumission_asso_produits(sID VARCHAR(24),
ProductID int NOT NULL,
sQuantite int NOT NULL,
sTotal DECIMAL,
FOREIGN KEY (ProductID) REFERENCES produits(ID) ON DELETE CASCADE,
FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);

DELIMITER //
CREATE TRIGGER CalPrixTotalSoumission
    BEFORE INSERT ON soumission_asso_produits
    FOR EACH ROW
    BEGIN
        SET NEW.sTotal = (SELECT SUM(p.prix * NEW.sQuantite) FROM produits p WHERE p.ID = NEW.ProductID);
    END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AjouterSoumission(IN produitID int, IN qty int,IN soumissionID varchar(24))
BEGIN
    DECLARE total DECIMAL;    
    SET @sql := CONCAT("SELECT ProductID FROM soumission_asso_produits WHERE ProductID = ", produitID, " AND sID = '",soumissionID,"';");
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    IF FOUND_ROWS() > 0 THEN
        SET @sql := CONCAT("SELECT sQuantite into @tempQty FROM soumission_asso_produits WHERE ProductID = ", produitID, " AND sID = '",soumissionID,"';");
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SET @NewQty = qty + @tempQty;
        SET @sql := CONCAT("SELECT prix into @tempPrix FROM produits WHERE ID = ", produitID,";");
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SET total = @NewQty * @tempPrix;
        
        SET @sql := CONCAT("UPDATE soumission_asso_produits SET sQuantite = ",@NewQty,", sTotal = ",total," WHERE ProductID = ",produitID, " AND sID ='",soumissionID,"';");
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    ELSE
        SET @sql := CONCAT("SELECT prix into @tempPrix FROM produits WHERE ID = ", produitID,";");
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SET total = qty * @tempPrix;
        
        SET @sql := CONCAT("INSERT INTO soumission_asso_produits (sID, ProductID, sQuantite, sTotal) VALUES ('",soumissionID,"',",produitID,",",qty,",",total,");");
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AjouterPorte(IN categorie varchar(30), IN largeur int, IN hauteur int,IN isolation varchar(4),IN Motif int,IN Ferronerie varchar(24),IN Alliage varchar(24),IN prix int)
BEGIN
    INSERT INTO produits (TAG, catégorie, prix) VALUES ("porte",categorie, prix);
    SET @id_produit = LAST_INSERT_ID();
    INSERT INTO porte VALUES (@id_produit, largeur, hauteur, isolation, Motif, Ferronerie, Alliage);
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AjouterPanneaux(IN categorie varchar(30), IN largeur int, IN hauteur int,IN isolation varchar(4),IN Modele varchar(255),IN Alliage varchar(24),IN prix int)
BEGIN
    INSERT INTO produits (TAG, catégorie, prix) VALUES ("panneaux",categorie, prix);
    SET @id_produit = LAST_INSERT_ID();
    INSERT INTO panneaux VALUES (@id_produit, largeur, hauteur, isolation, Modele, Alliage);
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AjouterFerronnerie(IN categorie varchar(30), IN largeur int, IN hauteur int,IN Diametre varchar(6),IN Type varchar(24),IN prix int)
BEGIN
    INSERT INTO produits (TAG, catégorie, prix) VALUES ("ferronnerie",categorie, prix);
    SET @id_produit = LAST_INSERT_ID();
    INSERT INTO ferronnerie VALUES (@id_produit, largeur, hauteur, Diametre, Type);
END//
DELIMITER ;

-- DELIMITER //
-- CREATE TRIGGER porte_insert 
-- BEFORE INSERT ON porte 
-- FOR EACH ROW
-- BEGIN
--   INSERT INTO produits (produit) VALUES ('porte');
--   SET NEW.ID = LAST_INSERT_ID();
--   SET NEW.TAG = 'PORTE DE GARAGE';
-- END//
-- DELIMITER ;

-- DELIMITER //
-- CREATE TRIGGER panneau_insert 
-- BEFORE INSERT ON panneaux 
-- FOR EACH ROW
-- BEGIN
--   INSERT INTO produits (produit) VALUES ('panneaux');
--   SET NEW.ID = LAST_INSERT_ID();
--   SET NEW.TAG = 'PANNEAUX';
-- END//
-- DELIMITER ;

-- DELIMITER //
-- CREATE TRIGGER ferro_insert 
-- BEFORE INSERT ON ferronnerie 
-- FOR EACH ROW
-- BEGIN
--   INSERT INTO produits (produit) VALUES ('ferronnerie');
--   SET NEW.ID = LAST_INSERT_ID();
--   SET NEW.TAG = 'FERRONNERIE';
-- END//
-- DELIMITER ;



-- INSERT INTO Vehicle (vehicle_type, common_attribute1, common_attribute2)
-- VALUES ('Car', 'Value1', 'Value2');

-- -- Get the ID of the inserted Vehicle
-- SET @last_vehicle_id = LAST_INSERT_ID();

-- -- Insert into Car table
-- INSERT INTO Car (vehicle_id, car_specific_attribute)
-- VALUES (@last_vehicle_id, 'Car specific value');

-- CREATE TABLE soumission_asso_porte(sID VARCHAR(24),
-- ProductID int NOT NULL,
-- sQuantite int NOT NULL,
-- sTotal DECIMAL,
-- FOREIGN KEY (ProductID) REFERENCES porte(ID) ON DELETE CASCADE,
-- FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);

-- CREATE TABLE soumission_asso_panneaux(sID VARCHAR(24),
-- ProductID int NOT NULL,
-- sQuantite int NOT NULL,
-- sTotal DECIMAL,
-- FOREIGN KEY (ProductID) REFERENCES panneaux(ID) ON DELETE CASCADE,
-- FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);

-- CREATE TABLE soumission_asso_ferronnerie(sID VARCHAR(24),
-- ProductID int NOT NULL,
-- sQuantite int NOT NULL,
-- sTotal DECIMAL,
-- FOREIGN KEY (ProductID) REFERENCES ferronnerie(ID) ON DELETE CASCADE,
-- FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);


-- DELIMITER //
-- CREATE TRIGGER CalPrixTotalPanneau
--     BEFORE INSERT ON soumission_asso_panneaux
--     FOR EACH ROW
--     BEGIN
--         SET NEW.sTotal = (SELECT SUM(p.prix * NEW.sQuantite) FROM panneaux p WHERE p.ID = NEW.ProductID);
--     END //
-- DELIMITER ;

-- DELIMITER //
-- CREATE TRIGGER CalPrixTotalPorte
--     BEFORE INSERT ON soumission_asso_porte
--     FOR EACH ROW
--     BEGIN
--         SET NEW.sTotal = (SELECT SUM(p.prix * NEW.sQuantite) FROM porte p WHERE p.ID = NEW.ProductID);
--     END //
-- DELIMITER ;

-- DELIMITER //
-- CREATE TRIGGER CalPrixTotalFerronnerie
--     BEFORE INSERT ON soumission_asso_ferronnerie
--     FOR EACH ROW
--     BEGIN
--         SET NEW.sTotal = (SELECT SUM(f.prix * NEW.sQuantite) FROM ferronnerie f WHERE f.ID = NEW.ProductID);
--     END //
-- DELIMITER ;