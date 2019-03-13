from flask import Flask
from control_panel.views import control_panel

# TODO: Configure upload folder
UPLOAD_FOLDER = './packages'

def create_app(config_file):
	app = Flask(__name__) # Create application object
	app.config.from_pyfile(config_file) # Configure application
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	app.register_blueprint(control_panel) # Register control panel
	app.config['SESSION_TYPE'] = 'memcached'
	app.config['SECRET_KEY'] = 'super secret key'
	return app


if __name__ == '__main__':
	app = create_app('config.py') # Create application with config.py
	app.run(debug=True) # Run Flask application
