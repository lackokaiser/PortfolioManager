CREATE DATABASE CSFoundations;

use CSFoundations; 

CREATE TABLE stockdemotwo (
	transaction_id BIGINT auto_increment PRIMARY KEY NOT NULL,
    ticker VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    value DECIMAL,
    quantity DECIMAL,
    transaction_date DATE DEFAULT (now())
);
