CREATE DATABASE CSFoundations;

use CSFoundations; 

CREATE TABLE stockdemo (
	transaction_id BIGINT PRIMARY KEY NOT NULL,
    ticker VARCHAR(15) NOT NULL,
    name VARCHAR(15) NOT NULL,
    value DECIMAL,
    quantity DECIMAL,
    transaction_date DATE DEFAULT (now())
);
