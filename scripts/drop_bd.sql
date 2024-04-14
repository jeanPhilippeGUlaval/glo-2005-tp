USE dev;
DROP TABLE soumission_asso_produits;
DROP TABLE soumission_ids;
DROP TABLE users;
DROP TABLE porte;
DROP TABLE ferronnerie;
DROP TABLE panneaux;
DROP TABLE produits;

DROP PROCEDURE AjouterSoumission;
DROP PROCEDURE AjouterPorte;
DROP PROCEDURE AjouterPanneaux;
DROP PROCEDURE AjouterFerronnerie;

DROP DATABASE dev;


-- Rouler se code si jamais un problème de contraintes apparait en droppant la BD REMPLACER LE NOM DE LA TABLE--
-- USE INFORMATION_SCHEMA;
-- SELECT TABLE_NAME,
--        COLUMN_NAME,
--        CONSTRAINT_NAME,
--        REFERENCED_TABLE_NAME,
--        REFERENCED_COLUMN_NAME
-- FROM KEY_COLUMN_USAGE
-- WHERE TABLE_SCHEMA = "dev" 
--       AND TABLE_NAME = "porte" 
--       AND REFERENCED_COLUMN_NAME IS NOT NULL;