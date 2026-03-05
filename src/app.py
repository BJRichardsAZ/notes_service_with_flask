from flask import Flask
from src.db import close_db
from src.blueprints.notes import bp
from src.errors import register_error_handlers
import os

def create_app(test_config=None):
    app = Flask(__name__)

    #create a reference to the db in config for ease
    app.config['DATABASE'] = os.path.join(app.root_path, 'notes.db')

    if test_config is not None:
        app.config.update(test_config)

    register_error_handlers(app)

    app.register_blueprint(bp)

    app.teardown_appcontext(close_db)

    return app


# Create the global app instance for running directly
app = create_app()

# write a cli command for initializing (or recreating fresh) the tables from schema file 
from src.db import init_db
@app.cli.command('init_db')
def init_db_command():
    """CLI Command to Initialize Tables"""
    with app.app_context():   
        init_db()
    print("Initialized the database")

if __name__ == '__main__':
    app.run(debug=True)
