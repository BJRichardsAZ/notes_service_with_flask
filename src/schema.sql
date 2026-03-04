 -- notes table schema
 CREATE TABLE IF NOT EXISTS notes (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        content VARCHAR(250) NOT NULL,
        createdAt timestamp DEFAULT CURRENT_TIMESTAMP
        )