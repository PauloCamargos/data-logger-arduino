CREATE SCHEMA arduinoProject;

-- CHECK, DEFAULT
CREATE TABLE arduinoProject.environment(
	id SERIAL PRIMARY KEY ,
	description VARCHAR(64) NOT NULL
);

CREATE TABLE arduinoProject.users(
	id SERIAL PRIMARY KEY,
	usr_full_name VARCHAR(256) NOT NULL,
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
	id_envrmt INT,
	read_value NUMERIC (5,2) NOT NULL CHECK (read_value > 0),
	CONSTRAINT fk_user FOREIGN KEY (id_user) REFERENCES arduinoProject.users (id),
	CONSTRAINT fk_envrmt FOREIGN KEY (id_envrmt) REFERENCES arduinoProject.environment (id)
);

CREATE TABLE arduinoProject.history (
	id SERIAL PRIMARY KEY,
	id_msr INT,
	msr_date DATE,
	msr_hour TIME,
	CONSTRAINT fk_msr FOREIGN KEY (id_msr) REFERENCES arduinoProject.measures (id)
)
