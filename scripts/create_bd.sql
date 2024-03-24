CREATE DATABASE dev;
USE dev;
CREATE TABLE users(id int PRIMARY KEY AUTO_INCREMENT, email varchar(256), password varchar(256));
CREATE TABLE color (colorId int PRIMARY KEY, colorName varchar(25));
CREATE TABLE bundle (bundleID int PRIMARY KEY, bundleName varchar(25));
CREATE TABLE porte_id_gen(numerical_id INT AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE porte (ID VARCHAR(24) PRIMARY KEY, bundleID int, Catégorie varchar(30), Largeur int, Hauteur int, isolation varchar(4), Motif int, Ferronerie varchar(24), Alliage varchar(24), Prix int, FOREIGN KEY (bundleID) REFERENCES bundle(bundleID));
CREATE TABLE bundle_asso_color (bundleID int, colorId int, PRIMARY KEY (bundleID, colorId), FOREIGN KEY (bundleID) REFERENCES bundle(bundleID), FOREIGN KEY (colorId) REFERENCES color(colorId));
CREATE TABLE soumission_ids (ID VARCHAR(24) PRIMARY KEY);
CREATE TABLE soumission (ID VARCHAR(24), Produit VARCHAR(24),  Catégorie varchar(30), Prix int, FOREIGN KEY (ID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);

DELIMITER //
CREATE TRIGGER porte_insert 
BEFORE INSERT ON porte 
FOR EACH ROW
BEGIN
  INSERT INTO porte_id_gen VALUES (NULL);
  SET NEW.ID = CONCAT('PORTE-',(LAST_INSERT_ID()));
END//
DELIMITER ;


INSERT INTO soumission_ids VALUES ("Soumission_1");
INSERT INTO soumission VALUES ("Soumission_1", "PORTE-1","CABANON", 800);

DELETE FROM soumission_ids WHERE ID = 'Soumission_1';