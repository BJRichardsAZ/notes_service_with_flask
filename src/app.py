from flask import Flask
from src.db import close_db
from src.blueprints.notes import bp
from src.errors import register_error_handlers
import os

def create_app(test_config=None):
    app = Flask(__name__)

    #needed to change this so that in docker data is actually saved in the volume, outside of test enviroment we grab env variable for path
    if test_config is not None:
        app.config.update(test_config)
    else:
        app.config['DATABASE'] = os.getenv('DATABASE', os.path.join(app.root_path, 'notes.db'))
    register_error_handlers(app)

    app.register_blueprint(bp)

    app.teardown_appcontext(close_db)

    return app


#create the global app instance for running directly
app = create_app()

#write a cli command for initializing (or recreating fresh) the tables from schema file 
from src.db import init_db
@app.cli.command('init_db')
def init_db_command():
    """CLI Command to Initialize Tables"""
    with app.app_context():   
        init_db()
    print("Initialized the database")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
