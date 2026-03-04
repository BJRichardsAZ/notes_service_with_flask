from flask import Flask, jsonify, request, g 
import sqlite3 
import os 
from errors import register_error_handlers

def create_app():
    app = Flask(__name__)

    #create a reference to the db in config for ease
    app.config['DATABASE'] = os.path.join(app.root_path, 'notes.db')
    register_error_handlers(app)

    return app


app = create_app()


#create a fresh lazy connection instance for each http request using per-request bag
#provided by flask 
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            #detect data types
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

# function for initializing the tables based on the sql create statement stored in schema.sql
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
    db = g.pop('db', None)
    if db is not None:
        db.close()

#create route for REST "notes endpoint", add methods for both get and post 
@app.route('/notes', methods = ['GET', 'POST'])
def notes():
        if request.method == 'POST':
            # throw error if missing input parameters
            if 'content' not in request.form:
                raise MissingParameter()
            content = request.form['content']
            db = get_db()
            db.execute(
                'INSERT INTO notes (content) VALUES (?)',
                (content,)
            )
            db.commit()
            return jsonify({
                "success": True,
                "message": "Note added succesfully!"
            }), 201
        elif request.method == 'GET':
            db = get_db()
            notes = db.execute(
                'SELECT * FROM notes'
            ).fetchall()
            return jsonify({
                "success": True,
                "message": "Notes grabbed succesfully!",
                "notes": [dict(note) for note in notes]
            })
   
   #create route for REST endpoint for operating on specific nods, add methods for both get and post, and update
@app.route('/notes/{id}', methods = ['GET', 'DELETE'])
def note(id):
 
        if request.method == 'GET':
            db = get_db()
            note = db.execute(
                'SELECT * FROM notes WHERE id = ?',
                (id,)
            ).fetchone()
            if note is None:
                return NoteNotFound()
            else: return jsonify({
                "success": True,
                "message": "Note grabbed succesfully!",
                "note": dict(note)
            }), 201 
        if request.method == 'DELETE':
            db = get_db()
            cursor = db.execute(
                'DELETE FROM notes WHERE id = ?',
                (id,)
            )
            db.commit()

            if cursor.rowcount == 0:
               raise NoteNotFound()

            return jsonify({
                "success": True,
                "message": "Note deleted succesfully!"
            })
   

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)

