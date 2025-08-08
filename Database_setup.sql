CREATE DATABASE CSFoundations;

use CSFoundations; 

CREATE TABLE stockdemo (
	transaction_id BIGINT auto_increment PRIMARY KEY,
    ticker VARCHAR(50) NOT NULL,
    stock_name VARCHAR(50) NOT NULL,
    stock_value DECIMAL(12,3) NOT NULL,
    quantity DECIMAL(12,3) NOT NULL,
    transaction_date DATE DEFAULT (now())
    );