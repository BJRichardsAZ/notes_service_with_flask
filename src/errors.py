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

class InvalidNoteLength(Exception): 
    status_code = 422 

    def __init__(self, message= "Content parameter was over the 250 character limit."):
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
    
    #custom handler for missing parameters in request
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
    
    #custom handler for content being to long
    @app.errorhandler(InvalidNoteLength)
    def handle_invalid_note_length(e):
        return jsonify({
            "success": False,
            "error": str(e)
        }), 422
    
    #catch all handler for http errors 
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            "success": False,
            "error": e.description
        }), e.code
    
    #catch all handler for other exceptions
    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        return jsonify({
            "success": False,
            "error": "Internal Server Error"
        }), 500
    
