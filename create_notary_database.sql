CREATE DATABASE notary_database;
USE notary_database;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(150) UNIQUE,
    password VARCHAR(150),
    notary_id INT
);

CREATE TABLE notary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    address VARCHAR(150),
    address2 VARCHAR(150),
    city VARCHAR(150),
    state VARCHAR(150),
    zip_code VARCHAR(150),
    email VARCHAR(150) UNIQUE,
    password VARCHAR(150),
    cert_no VARCHAR(150),
    user_id INT
);

CREATE TABLE document (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150),
    description VARCHAR(150),
    encrypted_data LONGBLOB,
    file LONGBLOB,
    hash_value VARCHAR(64) NOT NULL,
    user_id INT NOT NULL
);

CREATE TABLE user_document (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    document_id INT,
    notary_id INT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notary_document (
    id INT AUTO_INCREMENT PRIMARY KEY,
    notary_id INT,
    document_id INT,
    user_id INT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE form_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    addr VARCHAR(150) NOT NULL,
    city VARCHAR(150) NOT NULL,
    st VARCHAR(2) NOT NULL,
    zipcode VARCHAR(12) NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    uploaded_file VARCHAR(255) NOT NULL
);

ALTER TABLE user
ADD CONSTRAINT FK_user_notary
FOREIGN KEY (notary_id) REFERENCES notary(id);

ALTER TABLE notary
ADD CONSTRAINT FK_notary_user
FOREIGN KEY (user_id) REFERENCES user(id);

ALTER TABLE document
ADD CONSTRAINT FK_document_user
FOREIGN KEY (user_id) REFERENCES user(id);

ALTER TABLE user_document
ADD CONSTRAINT FK_user_document_user
FOREIGN KEY (user_id) REFERENCES user(id),
ADD CONSTRAINT FK_user_document_document
FOREIGN KEY (document_id) REFERENCES document(id),
ADD CONSTRAINT FK_user_document_notary
FOREIGN KEY (notary_id) REFERENCES notary(id);

ALTER TABLE notary_document
ADD CONSTRAINT FK_notary_document_notary
FOREIGN KEY (notary_id) REFERENCES notary(id),
ADD CONSTRAINT FK_notary_document_document
FOREIGN KEY (document_id) REFERENCES document(id),
ADD CONSTRAINT FK_notary_document_user
FOREIGN KEY (user_id) REFERENCES user(id);

ALTER TABLE form_data
ADD CONSTRAINT FK_form_data_user
FOREIGN KEY (user_id) REFERENCES user(id);

-- Insert 10 sample users
INSERT INTO user (first_name, last_name, email, password) VALUES
('John', 'Doe', 'john.doe@example.com', 'securepassword1'),
('Jane', 'Smith', 'jane.smith@example.com', 'securepassword2'),
('Alice', 'Johnson', 'alice.johnson@example.com', 'securepassword3'),
('Bob', 'Williams', 'bob.williams@example.com', 'securepassword4'),
('Charlie', 'Brown', 'charlie.brown@example.com', 'securepassword5'),
('David', 'Jones', 'david.jones@example.com', 'securepassword6'),
('Eva', 'Garcia', 'eva.garcia@example.com', 'securepassword7'),
('Frank', 'Miller', 'frank.miller@example.com', 'securepassword8'),
('Grace', 'Lee', 'grace.lee@example.com', 'securepassword9'),
('Hank', 'Martinez', 'hank.martinez@example.com', 'securepassword10');

-- Insert 2 sample notaries
INSERT INTO notary (first_name, last_name, address, address2, city, state, zip_code, email, password, cert_no) VALUES
('Laura', 'Davis', '123 Main St', 'Apt 4B', 'New York', 'NY', '10001', 'laura.davis@example.com', 'notarypassword1', '123456'),
('Sam', 'Taylor', '789 Broadway', 'Suite 3', 'Los Angeles', 'CA', '90001', 'sam.taylor@example.com', 'notarypassword2', '789012');

-- Insert Sample documents data
INSERT INTO document (title, description, hash_value, user_id) VALUES
('Document 1', 'Sample document 1', 'a1b2c3d4e5f6g7h1', 1),
('Document 2', 'Sample document 2', 'a1b2c3d4e5f6g7h2', 2),
('Document 3', 'Sample document 3', 'a1b2c3d4e5f6g7h3', 3),
('Document 4', 'Sample document 4', 'a1b2c3d4e5f6g7h4', 4),
('Document 5', 'Sample document 5', 'a1b2c3d4e5f6g7h5', 5),
('Document 6', 'Sample document 6', 'a1b2c3d4e5f6g7h6', 6),
('Document 7', 'Sample document 7', 'a1b2c3d4e5f6g7h7', 7),
('Document 8', 'Sample document 8', 'a1b2c3d4e5f6g7h8', 8),
('Document 9', 'Sample document 9', 'a1b2c3d4e5f6g7h9', 9);

-- Insert Sample form e-notary data 
INSERT INTO form_data (user_id, addr, city, st, zipcode, document_type, uploaded_file) VALUES
(1, '123 Elm St', 'New York', 'NY', '10001', 'Contract', 'document1.pdf'),
(2, '456 Oak St', 'Los Angeles', 'CA', '90001', 'Agreement', 'document2.pdf'),
(3, '789 Pine St', 'Chicago', 'IL', '60601', 'Invoice', 'document3.pdf'),
(4, '321 Maple St', 'Houston', 'TX', '77001', 'Contract', 'document4.pdf'),
(5, '654 Birch St', 'Phoenix', 'AZ', '85001', 'Agreement', 'document5.pdf'),
(6, '987 Spruce St', 'Philadelphia', 'PA', '19101', 'Invoice', 'document6.pdf'),
(7, '147 Cedar St', 'San Antonio', 'TX', '78201', 'Contract', 'document7.pdf'),
(8, '258 Willow St', 'San Diego', 'CA', '92101', 'Agreement', 'document8.pdf'),
(9, '369 Redwood St', 'Dallas', 'TX', '75201', 'Invoice', 'document9.pdf'),
(10, '481 Poplar St', 'San Jose', 'CA', '95101', 'Contract', 'document10.pdf');

-- Insert user_document records
INSERT INTO user_document (user_id, document_id, notary_id) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 4, 1),
(5, 5, 1),
(6, 6, 2),
(7, 7, 2),
(8, 8, 2),
(9, 9, 2);

-- Insert notary_document records
INSERT INTO notary_document (notary_id, document_id, user_id) VALUES
(1, 1, 1),
(1, 2, 2),
(1, 3, 3),
(1, 4, 4),
(1, 5, 5),
(2, 6, 6),
(2, 7, 7),
(2, 8, 8),
(2, 9, 9);

-- A list of users combined with their form data
SELECT u.id as user_id, u.first_name, u.last_name, u.email, fd.*
FROM user u
JOIN form_data fd ON u.id = fd.user_id;

-- Add a status column

-- Update status once the document has been notarized

-- A list of users along with the number of documents they submited

-- a list of notaries along with the number of documents they have 
-- notarized and the number of documents pending notarization

-- a list of document types along with the number of documents for each type




