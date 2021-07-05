from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app= Flask(__name__)
app.config['SECRET_KEY']='meowmeow'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt= Bcrypt(app)
from flask_mail import Mail

db = SQLAlchemy(app)
login_manager= LoginManager(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "ms9296@srmist.edu.in"
app.config['MAIL_PASSWORD'] = "Saikor@5277"
mail = Mail(app)

from ownblog import routes
from ownblog.models import User,Post


