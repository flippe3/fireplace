# create database
CREATE DATABASE firedb;

# choose database to use
USE firedb;

# create the table for the users, the long varchar for token is especially relevant
CREATE table users(
name VARCHAR(100) NOT NULL,
token VARCHAR(200) NOT NULL,
password VARCHAR(100) NOT NULL,
role ENUM("admin","user"),
salt VARCHAR(100),
PRIMARY KEY(name)
);

# create the table for the fireplaces
CREATE table fireplaces(
id MEDIUMINT NOT NULL AUTO_INCREMENT,
name VARCHAR(100) NOT NULL,
latitude DECIMAL(9,6),
longitude DECIMAL(9,6),
wood BOOLEAN,
image VARCHAR(200) DEFAULT 'placeholder.png',
PRIMARY KEY(id)
);

# insert some exemplary fireplaces, more are supposed to be added by the prosumers
INSERT INTO fireplaces (name, latitude, longitude, wood) VALUES ("Birdtower",65.633053,22.093550,TRUE);
INSERT INTO fireplaces (name, latitude, longitude, wood) VALUES ("Birdtower",65.633061,22.093837,TRUE);
INSERT INTO fireplaces (name, latitude, longitude, wood) VALUES ("University",65.616458,22.140533,TRUE);
INSERT INTO fireplaces (name, latitude, longitude, wood) VALUES ("Gültzauuddens badplats",65.587876,22.125135,TRUE);
INSERT INTO fireplaces (name, latitude, longitude, wood) VALUES ("Utkik Grönnan",65.625557,22.094312,TRUE);

# basic request methods for database
SELECT * FROM users;
SELECT * FROM fireplaces;