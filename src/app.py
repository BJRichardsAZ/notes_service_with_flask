from flask import Flask
import sqlite3 
import os 


app = Flask(__name__)

#create a reference to the db in config for ease
app.config['DATABASE'] = os.path.join(app.root_path, 'notes.db')

#create a fresh lazy connection instance for each http request using per-request bag
#provided by flask 
def get_db():
    if 'db' not in app.extensions:
        app.extensions['db'] = sqlite3.connect(
            app.config['DATABASE'],
            #detect data types
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        app.extensions['db'].row_factory = sqlite3.Row
    return app.extensions['db']

# function route for initializimg the tables based on the sql create statement stored in schema.sql
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()
        print('Database initialized');

# write a cli command for initializing the tables from schema file 
@app.cli.command('init_db')
def init_db_command():
    """CLI Command to Initialize Tables"""
    init_db()
    print("Initialized the database")


#at the end of a request, close the opened db connection explicitly 
@app.teardown_appcontext
def close_db(e=None):
    db = app.extensions.pop('db', None)
    if db is not None:
        db.close()

