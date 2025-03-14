-- Create the database
CREATE DATABASE IF NOT EXISTS user_db;

-- Switch to the database
USE user_db;

-- Create atm_users table
CREATE TABLE IF NOT EXISTS atm_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    pin VARCHAR(10) NOT NULL,
    balance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    account_number VARCHAR(20) NOT NULL,
    description VARCHAR(255) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_number) REFERENCES atm_users(account_number)
);



/* 
Key features of this schema:

1. Database named user_db

2. atm_users table:
    Auto-incrementing primary key id

    Unique account numbers and emails

    PIN stored as VARCHAR(10)

    Balance with 2 decimal places (₹0.00 default)

    Automatic timestamp for account creation

3. transactions table:

    Auto-incrementing primary key

    Foreign key relationship with atm_users

    Transaction description field

    Automatic timestamp for transactions


To set this up:
    Run these commands in MySQL client

    Make sure your MySQL user has creation privileges

    The order matters - create atm_users first since transactions references it


You can then insert test users with:
    INSERT INTO atm_users (account_number, email, pin, balance) 
    VALUES ('123456789', 'user@example.com', '1234', 1000.00);
*/