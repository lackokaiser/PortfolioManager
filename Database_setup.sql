CREATE DATABASE CSFoundations;

use CSFoundations; 

CREATE TABLE stockdemo (
	transaction_id BIGINT auto_increment PRIMARY KEY,
    ticker VARCHAR(50) NOT NULL,
    stock_name VARCHAR(50) NOT NULL,
    stock_price DECIMAL NOT NULL,
    quantity DECIMAL NOT NULL,
    transaction_date DATE DEFAULT (now())
    );
