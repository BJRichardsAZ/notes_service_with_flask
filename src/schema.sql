 -- notes table schema
 CREATE TABLE NOTES (
        id INT AUTO_INCREMENT PRIMARY KEY,
        content VARCHAR(250) NOT NULL,
        createdAt timestamp DEFAULT CURRENT_TIMESTAMP,
        )