CREATE SCHEMA arduinoProject;

CREATE TABLE arduinoProject.environment(
	id SERIAL PRIMARY KEY ,
	description VARCHAR(64) NOT NULL
);

CREATE TABLE arduinoProject.users(
	id SERIAL PRIMARY KEY,
	usr_fullname VARCHAR(256) NOT NULL,
	usr_contact VARCHAR(64) NOT NULL,
	username VARCHAR(64) UNIQUE NOT NULL,
	pswd VARCHAR(64) NOT NULL,
	active BOOLEAN DEFAULT 't'
);

CREATE TABLE arduinoProject.physical_quantity(
	id SERIAL PRIMARY KEY,
	description VARCHAR(32) NOT NULL,
	unity VARCHAR(32) NOT NULL
);

CREATE TABLE arduinoProject.measures(
	id SERIAL PRIMARY KEY,
	id_user INT,
	id_environment INT,
    id_pquantity INT,
	read_value NUMERIC(5,2) NOT NULL CHECK (read_value > 0),
	CONSTRAINT fk_user FOREIGN KEY (id_user) REFERENCES arduinoProject.users (id),
	CONSTRAINT fk_envrmt FOREIGN KEY (id_environment) REFERENCES arduinoProject.environment (id),
	CONSTRAINT fk_pqnty FOREIGN KEY (id_pquantity) REFERENCES arduinoProject.physical_quantity (id)
);

CREATE TABLE arduinoProject.history (
	id SERIAL PRIMARY KEY,
	id_msr INT,
	record_date TIMESTAMP,
    action TEXT,
	CONSTRAINT fk_msr FOREIGN KEY (id_msr) REFERENCES arduinoProject.measures (id)
)

DROP TABLE arduinoproject.history;
DROP TABLE arduinoproject.measures;
DROP TABLE arduinoproject.physical_quantity;
DROP TABLE arduinoproject.teste ;
DROP TABLE arduinoproject.users;
DROP TABLE arduinoproject.environment ;

INSERT INTO arduinoproject.users(usr_fullname, usr_contact, username, pswd)
VALUES  ('Thiago Pereira de Oliveira', 'thiago@ufu.br', 'thiagopo', 'admin'),
	('Paulo Camargos Silva', 'paulo@ufu.br', 'paulocs','123456'),
	('Pablo Nunes', 'pablo@ufu.br', 'pablon','senha'),
	('Marcio Cunha', 'marcio@ufu.br', 'marioc', 'password123');

SELECT * FROM arduinoproject.measures;
SELECT * FROM arduinoproject.environment;
SELECT * FROM arduinoproject.physical_quantity;
SELECT read_value FROM arduinoproject.measures;

DELETE FROM arduinoproject.environment;
DELETE FROM arduinoproject.measures;
DELETE FROM arduinoproject.physical_quantity;

UPDATE arduinoproject.physical_quantity SET description='Humidity' WHERE id=2;

SELECT m.id AS id_measure, u.usr_fullname , m.read_value, p.unity, e.description
FROM arduinoproject.measures m
INNER JOIN arduinoproject.users u ON m.id_user = u.id
INNER JOIN arduinoproject.physical_quantity p ON m.id_pquantity = p.id
INNER JOIN arduinoproject.environment e ON m.id_environment = e.id
ORDER BY m.id ASC;

ALTER TABLE arduinoproject.measures
DROP CONSTRAINT measures_read_value_check;

ALTER TABLE arduinoproject.measures ADD CONSTRAINT
measures_read_value_check CHECK (read_value > -1);
