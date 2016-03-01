from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a super secure key"


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://profile:newp@localhost/profile"
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)


from app import views
