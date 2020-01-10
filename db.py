from flask import Flask,render_template,request,flash,redirect,url_for
from flask_login import LoginManager,UserMixin,login_user,login_required,current_user,logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask import Flask, render_template, redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property
import cgi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret'
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

class BranchMaster(db.Model):
	id    = db.Column(db.Integer, primary_key=True)
	place = db.Column(db.String(30), unique=True)
	city  = db.Column(db.String(30))
	state = db.Column(db.String(30))

class DesignationMaster(db.Model):
	code    = db.Column(db.Integer, primary_key=True)
	designation = db.Column(db.String(30), unique=True)

class DepartmentMaster(db.Model):
	code    = db.Column(db.Integer, primary_key=True)
	department = db.Column(db.String(30), unique=True)

class UserMaster(db.Model):
	user_code    = db.Column(db.Integer, primary_key=True)
	Username = db.Column(db.String(30), unique=True)
	branchname = db.Column(db.String(30))
	designation = db.Column(db.String(30))
	department = db.Column(db.String(30))

class InvoiceMaster(db.Model):
	invoicecode = db.Column(db.Integer,primary_key=True)
	invoicename = db.Column(db.String(30),unique=True)
	user_code = db.Column(db.String(30),unique=True,)
	usertype = db.Column(db.String(30),unique=True)

class TaxMaster(db.Model):
	taxcode = db.Column(db.Integer,primary_key=True)
	taxname = db.Column(db.String(30),unique=True)
	taxpercent = db.Column(db.Float(8))
