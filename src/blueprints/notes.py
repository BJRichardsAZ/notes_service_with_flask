from flask import Blueprint, jsonify, request
from src.errors import MissingParameter, InvalidNoteLength, NoteNotFound, register_error_handlers
from src.db import get_db, init_db

bp = Blueprint('/notes', __name__)


#create route for REST "notes endpoint", add methods for both get and post 
@bp.route('/notes', methods = ['GET', 'POST'])
def notes():
        if request.method == 'POST':

            # throw error if missing input parameters or content length is too long
            content = request.values.get('content')
            if content is None:
                raise MissingParameter()
            if content == '':
                raise MissingParameter()
            if len(content) > 250:
                raise InvalidNoteLength()
            
            #db operations
            db = get_db()
            db.execute(
                'INSERT INTO notes (content) VALUES (?)',
                (content,)
            )
            db.commit()
            
            #return success message
            return jsonify({
                "success": True,
                "message": "Note added succesfully!"
            }), 200
        
        db = get_db()
        notes = db.execute(
            'SELECT * FROM notes'
        ).fetchall()
        return jsonify({
            "success": True,
            "message": "Notes grabbed succesfully!",
            "notes": [dict(note) for note in notes]
        }), 200
        
#create route for REST endpoint for operating on specific nods, add methods for both get and post, and update
@bp.route('/notes/<id>', methods = ['GET', 'DELETE'])
def note(id):
        if request.method == 'GET':
            db = get_db()
            note = db.execute(
                'SELECT * FROM notes WHERE id = ?',
                (id,)
            ).fetchone()
            #check for not existance
            if note is None:
                raise NoteNotFound()
            else: return jsonify({
                "success": True,
                "message": "Note grabbed succesfully!",
                "note": dict(note)
            }), 200 
        if request.method == 'DELETE':
            db = get_db()
            cursor = db.execute(
                'DELETE FROM notes WHERE id = ?',
                (id,)
            )
            db.commit()
            #check for not existance, if rowcount is zero, that means the cursor found no match
            if cursor.rowcount == 0:
               raise NoteNotFound()

            return jsonify({
                "success": True,
                "message": "Note deleted succesfully!"
            })