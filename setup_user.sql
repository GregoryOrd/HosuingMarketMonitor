CREATE DATABASE housing;
CREATE USER 'retriever'@'localhost' IDENTIFIED BY 'SomePasswordHere';
GRANT ALL PRIVILEGES ON housing.* TO 'retriever'@'localhost';
FLUSH PRIVILEGES;