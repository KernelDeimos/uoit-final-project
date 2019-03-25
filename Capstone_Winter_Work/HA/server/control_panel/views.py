import os
import zipfile
import yaml, json
import shutil
from flask import Flask, current_app, Blueprint, render_template, request, flash, redirect, url_for, Response
from werkzeug.utils import secure_filename

from bindings import new_ll, connect, new_interpreter

# Create local interpreter and remote interpreter
ll = new_ll("../connective/connective/sharedlib/elconn.so")
ll.elconn_init(1)
# TODO: get Connective URL from configuration
remote_connective = connect(ll, b"http://vps.ericdube.com:3111")
# remote_connective = connect(ll, b"http://127.0.0.1:3003")
connective = new_interpreter(ll)
# Allow messages to be send to remote interpreter by prefixing
# the command "hub"
ll.elconn_link(b"hub", connective.ii, remote_connective.ii)


control_panel = Blueprint('control_panel', __name__)

PACKAGE_DIRECTORY = './packages'
ALLOWED_EXTENSIONS = ['zip']

# Control Panel Main Page
@control_panel.route('/')
def index():
	# TODO: Check packages name matches spec name
	# TODO: Clean up invalid packages
	# Get Upload Directory
	UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
	# Get list of current packages
	packages_dir = os.listdir(UPLOAD_FOLDER)
	# Get all package specifications
	packages = []
	for dir_name in packages_dir:
		dir = os.path.join(UPLOAD_FOLDER, dir_name)
		if os.path.isdir(dir):
			# Check if valid directory is a package
			package_dir = os.listdir(dir)
			for file in package_dir:
				if file == "package.yml":
					package_config = os.path.join(dir, file)
					with open(package_config, "r") as stream:
						try:
							package = yaml.load(stream)
						except Exception as exc:
							package = exc
					packages.append(package)
	# Get Devices
	# Update local store
	# TODO: set a timer for this instead of doing it on every request
	connective.runs(': devices (store (hub devices list))')

	# Copy devices list from Connective to Python
	devices = connective.runs('devices', tolist=True)
	
	return render_template("index.html", packages = packages, devices = devices)
	


# View Packages
@control_panel.route('/packages')
def view_packages():
	# TODO: Check packages name matches spec name
	# TODO: Clean up invalid packages
	# Get Upload Directory
	UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
	# Get list of current packages
	packages_dir = os.listdir(UPLOAD_FOLDER)
	# Get all package specifications
	packages = []
	for dir_name in packages_dir:
		dir = os.path.join(UPLOAD_FOLDER, dir_name)
		if os.path.isdir(dir):
			# Check if valid directory is a package
			package_dir = os.listdir(dir)
			for file in package_dir:
				if file == "package.yml":
					package_config = os.path.join(dir, file)
					with open(package_config, "r") as stream:
						try:
							package = yaml.load(stream)
						except Exception as exc:
							package = exc
					packages.append(package)
	# Create Context
	context = {"packages": packages, "devices": devices"}
	# Render View
	return render_template("view_packages.html", packages = packages)

# View Package
@control_panel.route('/packages/<package_name>')
def view_package(package_name):
	# Check for required paramter
	if package_name is not None:
		# Get Upload Directory
		UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
		# Get Package Directory
		package_dir = os.path.join(UPLOAD_FOLDER, package_name, "package.yml")
		# Get Package Config
		with open(package_dir, "r") as stream:
			try:
				package = yaml.load(stream)
				return render_template("view_package.html", package = package)
			except Exception as exc:
				exception = exc
				return render_template('error_template.html', exception = exception)
	# TODO: Throw actual exception
	else:
		return render_template("error_template.html", exception="Expected '/packages/<package_name>'. Got required parameter 'package_name' equal to None.")

# Helper method for add_package
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add Package
@control_panel.route('/packages/add', methods=['GET', 'POST'])
def add_package():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('Missing file')
			return render_template("add_package.html", error=request.files['file'])
		file = request.files['file']
		if file.filename == '':
			flash('No file selected')
			return render_template("add_package.html", error="No file selected")
		elif file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
			# TODO package set up
			return redirect('/packages/setup?package='+filename)

	return render_template("add_package.html")

# Setup Package
@control_panel.route('/packages/setup')
def setup_package():
	package = request.args.get('package')
	# Check for required parameter
	if package is not None:
		try:
			# Unzip package file
			# TODO: Prevent name collisions
			zip_ref = zipfile.ZipFile(os.path.join(current_app.config['UPLOAD_FOLDER'], package), mode='r')
			zip_ref = zip_ref.extractall(current_app.config['UPLOAD_FOLDER'])
			# Get Package instructions
			package_dir = package.rsplit('.')[0]
			config_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], package_dir, 'package.yml')
			with open(config_dir, "r") as stream:
				try:
					config = yaml.load(stream)
				except Exception as exc:
					return str(exc)

			# TODO: Add package instructions to jobs list
			# TODO: Add package specification to packages.yml

			return redirect('/packages')
		except Exception as exc:
			return render_template("error_template.html", exception=exc)
	# TODO: Throw real exception
	else:
		return render_template("error_template.html", exception="Expected query string 'package=<string>'. Got required query string 'package' equal to None.")

# Remove Package
@control_panel.route('/packages/remove/<package_name>')
def remove_package(package_name):
	# TODO Send kill command to Manager
	# Check for required paramter
	if package_name is not None:
		# Get Upload Directory
		UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
		package_dir = os.path.join(UPLOAD_FOLDER, package_name)
		# Remove Package
		try:
			shutil.rmtree(package_dir)
		except Exception as exc:
			return render_template("error_template.html", exception=exc)
		# Render success template
		return render_template("remove_package.html", removal=package_name)
	# TODO: Throw real exception
	else:
		return render_template("error_template.html", exception="Expected '/packages/remove/<package_name>'. Got required parameter 'package_name' equal to None.")

# View Devices
@control_panel.route('/devices')
def view_devices():
	# Update local store
	# TODO: set a timer for this instead of doing it on every request
	connective.runs(': devices (store (hub devices list))')

	# Copy devices list from Connective to Python
	devices = connective.runs('devices', tolist=True)

	return Response(json.dumps(devices), mimetype='application/json')

# View Macros
@control_panel.route('/macros')
def view_macros():
	pass

# Add Macro
@control_panel.route('/macros/add')
def add_macro():
	pass

# Remove Macro
@control_panel.route('/macros/remove')
def remove_macro():
	pass
