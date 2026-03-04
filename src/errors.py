from flask import jsonify
from werkzeug.exceptions import HTTPException

#custom exception classes

class NoteNotFound(Exception):
    status_code = 404

    def __init__(self, message= 'Note with that id not found.'):
        super().__init__()
        self.message = message

class MissingParameter(Exception):
    status_code = 400

    def __init__(self, message= 'Missing required parameter: content.'):
        super().__init__()
        self.message = message



#Error handlers
def register_error_handlers(app):
    #custom handler for note id that does not exist
    @app.errorhandler(NoteNotFound)
    def handle_note_not_found(e):
        return jsonify({
            "success": False,
            "error": str(e)
        }), e.status_code
    
    @app.errorhandler(MissingParameter)
    def handle_missing_parameter(e):    
        return jsonify({
            "success": False,
            "error": str(e)
        }), e.status_code
    
    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            "success": False,
            "error": "Not Found."
        }), 404
    
    #catch all handler for http errors 
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            "success": False,
            "error": e.description
        }), e.code
    
    #catch all for other exceptions
    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        return jsonify({
            "success": False,
            "error": "Internal Server Error"
        }), 500
    
