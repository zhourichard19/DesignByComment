from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
# initialize server
current_directory = os.getcwd()
statDir = current_directory+'/productivity/static/'
templateDir = current_directory+'/productivity/templates/'

app = Flask(__name__,static_folder=statDir,
            template_folder=templateDir)

# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '2cfcaeb21b9cfdceda6fda8e'
db = SQLAlchemy(app)

# Hashes passwords
bcrypt = Bcrypt(app)

# Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

# url tracker global vars
url_timestamp = {}
url_viewtime = {}
prev_url = ""

# loads routes
from productivity import routes