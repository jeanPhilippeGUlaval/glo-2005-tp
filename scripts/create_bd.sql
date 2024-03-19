CREATE DATABASE dev;
USE mysql;
CREATE USER 'user6'@'localhost' IDENTIFIED BY 'A4umTeF4B62*z3c3P*q!j9';
GRANT ALL PRIVILEGES ON *.* TO 'user6'@'localhost';
USE dev;
CREATE TABLE users(id int, email varchar(256), password varchar(256));