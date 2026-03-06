import sqlite3
from flask import g, current_app
#create a fresh lazy connection instance for each http request using per-request bag
#provided by flask 
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            #detect data types
            detect_types=sqlite3.PARSE_DECLTYPES,
            uri=True
        )
        g.db.row_factory = sqlite3.Row
    return g.db

# function for initializing the tables based on the sql create statement stored in schema.sql
def init_db():
        db = get_db()
        with current_app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()
        print('Database initialized');

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()