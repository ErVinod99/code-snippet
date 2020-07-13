from flask import Flask, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

from flask_mail import Mail, Message
from logging import FileHandler, WARNING

from flask_bcrypt import Bcrypt
from flask_login import LoginManager , login_required, logout_user, current_user, login_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from itsdangerous import URLSafeTimedSerializer, SignatureExpired


app = Flask(__name__)


file_handler = FileHandler('error_file.txt')
file_handler.setLevel(WARNING)

app.logger.addHandler(file_handler)



app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)

mail = Mail(app)

admin = Admin(app)

t = URLSafeTimedSerializer('SECRET_KEY')


from views import *

from models import *









if __name__=="__main__":
    app.run()