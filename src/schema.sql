 -- notes table schema
 -- existing table should be dropped if init_db is invoked while an instance already exists
 DROP TABLE IF EXISTS notes;

 CREATE TABLE IF NOT EXISTS notes (
       id INTEGER PRIMARY KEY,
        content VARCHAR(250) NOT NULL,
        createdAt timestamp DEFAULT CURRENT_TIMESTAMP
        )