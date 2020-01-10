from flask import Flask,render_template,request,flash,redirect,url_for,jsonify,abort
from logging import FileHandler, WARNING
from flask_login import LoginManager,UserMixin,login_user,login_required,current_user,logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta,datetime
from flask import Flask, render_template, redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField,DateField,IntegerField,FloatField,validators
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from wtforms.fields.html5 import DateField
from flask_uploads import UploadSet, configure_uploads, IMAGES , ALL
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy import func,cast,DATE,asc
import flask_excel as excel
import cgi
import pandas as pd
import sqlalchemy
import requests
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector
import json
from jsonmerge import merge
from jsonmerge import Merger



############ for whatsapp ########################################
wp = Flask(__name__)
wp.config['SECRET_KEY'] = 'secret'
wp.config.from_pyfile('wp.cfg')
wpp = SQLAlchemy(wp)

##################################################################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret'
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
photos = UploadSet('photos', ALL)
app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config.from_pyfile('config.cfg')
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=10)
configure_uploads(app, photos)
replies = []

file_handler = FileHandler('error_log.txt')
file_handler.setLevel(WARNING)

app.logger.addHandler(file_handler)

@app.route('/check',methods=['GET','POST'])
def check():
    return 1/0

'''@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        req_data = request.get_json()
        return req_data
      
    else:
        abort(400)
'''


class wp_response(wpp.Model):
    
    __bind_key__ ='response'
    __tablename__ ='whatsapp_response'
    
    index =wpp.Column(wpp.Integer, primary_key=True,autoincrement=True)
    unique_id = wpp.Column(wpp.Integer)
    mobile =  wpp.Column(wpp.String(500))
    text=wpp.Column(wpp.String(500))
    timestamp =wpp.Column(wpp.DateTime())
    type =wpp.Column(wpp.String(500))
    waNumber = wpp.Column(wpp.String(500))
    DATE = wpp.Column(wpp.String(50))
    Time = wpp.Column(wpp.String(50))
       
@app.route('/getreply',methods=['GET'])
def getrep():
    return jsonify({'replies' : replies})
    
    
@app.route('/webhook', methods=['POST'])
def apiroute():
    database_username = 'root'
    database_password = 'mercury@123'
    database_ip = '192.168.1.194'
    database_name = 'wp_demo'
    wp_connection = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(database_username,database_password, database_ip,database_name))
    reply = request.get_json(force=True)
    waNumber = None
    mobile = None
    replyId = None
    messageId = None
    timestamp = None
    type = None
    text = None
    mime_type = None
    signature = None
    url = None
    if 'mobile' in reply:
        mobile = reply['mobile']
        if len(mobile) == 12 and mobile.startswith('91'):
            mobile = mobile[2:]
            if 'waNumber' in reply:
                waNumber = reply['waNumber']
            if 'replyId' in reply:
                replyId = reply['waNumber']
            if 'messageId' in reply:
                messageId = reply['messageId']
            if 'timestamp' in reply:
                timestamp = reply['timestamp']
                timestamp = int(timestamp) / 1000
                timestamp = datetime.fromtimestamp(timestamp)
                date_time = str(timestamp)
                date = str(timestamp.date())
                time = str(timestamp.time())
            if 'type' in reply:
                type = reply['type']
            if 'mime_type' in reply:
                mime_type = reply['mime_type']
            if 'signature' in reply:
                signature = reply['signature']
            if 'url' in reply:
                url = reply['url']
            if 'text' in reply:
                text = reply['text']
            query = "SELECT reply_finished FROM `whatsapp_response` WHERE Mobile=%s AND DATE='%s' AND reply_finished='Y'"  % (mobile,date)
            with wp_connection.begin() as con:
                reply_finished = con.execute(query)
                print(reply_finished)
            print ('------------')
            for id in reply_finished:
                reply_finished = id[0]
                print(id)
            print ('-------------')
            print('reply_finished: %s' %reply_finished)
            if reply_finished == 'Y':
                abort(404)
            else:
                stmt = wp_response(
                mobile=mobile,
                text=text,
                timestamp=date_time,
                type=type,
                waNumber=waNumber,
                DATE=date,
                Time=time,
                )
                wpp.session.add(stmt)
                wpp.session.commit()

    return jsonify(request.get_json(force=True))
    
@app.route('/prodapi', methods=['POST'])
def prodapi():
    database_username = 'root'
    database_password = 'mercury@123'
    database_ip = '192.168.1.194'
    database_name = 'wp_demo'
    wp_connection = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(database_username,database_password, database_ip,database_name))
    reply = request.get_json(force=True)
    waNumber = None
    mobile = None
    replyId = None
    messageId = None
    timestamp = None
    type = None
    text = None
    mime_type = None
    signature = None
    url = None
    if 'mobile' in reply:
        mobile = reply['mobile']
        if len(mobile) == 12 and mobile.startswith('91'):
            mobile = mobile[2:]
            if 'waNumber' in reply:
                waNumber = reply['waNumber']
            if 'replyId' in reply:
                replyId = reply['waNumber']
            if 'messageId' in reply:
                messageId = reply['messageId']
            if 'timestamp' in reply:
                timestamp = reply['timestamp']
                timestamp = int(timestamp) / 1000
                timestamp = datetime.fromtimestamp(timestamp)
                date_time = str(timestamp)
                date = str(timestamp.date())
                time = str(timestamp.time())
            if 'type' in reply:
                type = reply['type']
            if 'mime_type' in reply:
                mime_type = reply['mime_type']
            if 'signature' in reply:
                signature = reply['signature']
            if 'url' in reply:
                url = reply['url']
            if 'text' in reply:
                text = reply['text']
            query = "SELECT reply_finished FROM `whatsapp_response` WHERE Mobile=%s AND DATE='%s' AND reply_finished='Y'"  % (mobile,date)
            branch_id = "SELECT id FROM `whatsapp_header` WHERE Mobile=%s AND ID IN (SELECT MAX(id) FROM whatsapp_header GROUP BY Mobile)" % (mobile)
            with wp_connection.begin() as con:
                reply_finished = con.execute(query)
                getting_branch = con.execute(branch_id)
                print(reply_finished)
            print ('------------')
            for id in reply_finished:
                reply_finished = id[0]
            
            branch_id_datas = 0
            
            for u_id in getting_branch:
                branch_id_datas = u_id[0]
               
         
            branch_id_data = int(branch_id_datas)
            print ('-------------')
            print('reply_finished: %s' %reply_finished)
            if reply_finished == 'Y':
                abort(404)
            else:
                stmt = wp_response(
                mobile=mobile,
                unique_id = branch_id_data,
                text=text,
                timestamp=date_time,
                type=type,
                waNumber=waNumber,
                DATE=date,
                Time=time,
                )
                wpp.session.add(stmt)
                wpp.session.commit()

    return jsonify(request.get_json(force=True))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

@login_manager.user_loader
def load_user(user_id):
    return UserMaster.query.get(user_id)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass']
        usern = UserMaster.query.filter_by(user_code=username).first()
        if usern is None:
            flash('Username is invalid')
            return render_template('login.html')
        login_user(usern, remember=True)
        if not usern:
            flash('Username is invalid')
            return render_template('login.html')
        if usern:
            if current_user.is_anonymous:
                flash('Please login properly')
                return render_template('login.html')
            if usern.Password != password:
                flash('Password is invalid')
                return render_template('login.html')
            if usern.Password == password:
                flash('')
                user = format(current_user.user_code)
                level = format(current_user.user_level)
                if level == "0":
                    return redirect(url_for('home'))
                elif level == "1":
                    return redirect(url_for('viewtransactionlevel'))
                else:
                    return redirect(url_for('flow_controlonly'))
                return render_template('home.html',usern=usern,user=user)
    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    user = format(current_user.Username)
    return render_template('home.html',user=user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')

#### BRANCH MASTER DETAILS ######
class BranchMaster(db.Model):
   code    = db.Column(db.Integer, primary_key=True)
   place = db.Column(db.String(30), unique=True)
   city  = db.Column(db.String(30))
   state = db.Column(db.String(30))

class Branchform(FlaskForm):
    branchname = StringField('Branch Name', validators=[InputRequired()])
    branchcity = StringField('Branch City', validators=[InputRequired()])
    branchstate = StringField('Branch State', validators=[InputRequired()])

@app.route('/branch', methods=['GET', 'POST'])
@login_required
def viewbranch():
   try:
      form = Branchform()
      if form.validate_on_submit():
         new_branch = BranchMaster(place=form.branchname.data, city=form.branchcity.data,state=form.branchstate.data)
         db.session.add(new_branch)
         db.session.commit()
         flash('Data added successfully')
   except exc.IntegrityError as e:
      db.session().rollback()
      flash('Branch already exists')
   branches = BranchMaster.query.all()
   user = format(current_user.Username)
   form.branchname.data = ""
   form.branchcity.data = ""
   form.branchstate.data = ""
   return render_template('branch.html', form=form,branches=branches,user=user)

#### Designation Master ######
class DesignationMaster(db.Model):
   code = db.Column(db.Integer, primary_key=True)
   designation = db.Column(db.String(30), unique=True)
   def __str__(self):
      return '{}'.format(self.designation)

class Designationform(FlaskForm):
    designationname = StringField('Designation Name', validators=[InputRequired()])

@app.route('/designation', methods=['GET', 'POST'])
@login_required
def viewDesignation():
   try:
      form = Designationform()
      if form.validate_on_submit():
         new_designation = DesignationMaster(designation=form.designationname.data)
         db.session.add(new_designation)
         db.session.commit()
         flash('Data added successfully')
   except exc.IntegrityError as e:
      db.session().rollback()
      flash('Designation already exists')
   user = format(current_user.Username)
   designations = DesignationMaster.query.all()
   form.designationname.data = ""
   return render_template('designation.html', form=form,designations=designations,user=user)

### DEPARTMENT MASTER ###
class DepartmentMaster(db.Model):
   code = db.Column(db.Integer, primary_key=True)
   department = db.Column(db.String(30), unique=True)
   def __repr__(self):
      return '{}'.format(self.department)

class Departmentform(FlaskForm):
    departmentname = StringField('Department Name', validators=[InputRequired()])

@app.route('/department', methods=['GET', 'POST'])
@login_required
def viewDepartment():
   try:
      form = Departmentform()
      if form.validate_on_submit():
         new_department = DepartmentMaster(department=form.departmentname.data)
         db.session.add(new_department)
         db.session.commit()
         flash('Data added successfully')

   except exc.IntegrityError as e:
      db.session().rollback()
      flash('Department already exists')
   user = format(current_user.Username)
   departments = DepartmentMaster.query.all()
   form.departmentname.data = ""
   return render_template('department.html', form=form, departments=departments,user=user)


### USER MASTER ###
class UserMaster(db.Model, UserMixin):
   user_code    = db.Column(db.String(10), primary_key=True)
   Username = db.Column(db.String(30))
   Password = db.Column(db.String(20))
   branchcode = db.Column(db.String(30))
   designationcode = db.Column(db.String(30))
   departmentcode = db.Column(db.String(30))
   user_level = db.Column(db.Integer())
   def get_id(self):
       return (self.user_code)

class usermasterform(FlaskForm):
   usercode = StringField('User Code', validators=[InputRequired()])
   username = StringField('User Name', validators=[InputRequired()])
   password = PasswordField('Password', validators=[InputRequired()])

@app.route('/user', methods=['GET', 'POST'])
@login_required
def viewusermaster():
   placename = request.form.get('branch_name', None)
   branch = db.session.query(BranchMaster.code).filter_by(place=placename).first()
   designame =request.form.get('designation', None)
   designationid = db.session.query(DesignationMaster.code).filter_by(designation=designame).first()
   depname = request.form.get('department', None)
   departmentid = db.session.query(DepartmentMaster.code).filter_by(department=depname).first()
   userlevel = request.form.get('userlevel',None)
   if userlevel == "Level 0":
       userlevel = 0
   elif userlevel == "Level 1":
       userlevel = 1
   elif userlevel == "Level 2":
       userlevel = 2
   elif userlevel == "Level 3":
       userlevel = 3
   elif userlevel == "Level 4":
       userlevel = 4
   else:
       userlevel = 5
   try:
       form = usermasterform()
       if form.validate_on_submit():
           new_user = UserMaster(user_code=form.usercode.data, Username=form.username.data, Password=form.password.data,branchcode=branch.code, designationcode=designationid.code,departmentcode=departmentid.code,user_level=userlevel)
           db.session.add(new_user)
           db.session.commit()
           flash('Data added successfully')
   except IntegrityError:
      db.session.rollback()
      flash('User already exists')
   details = db.session.query(UserMaster, BranchMaster, DesignationMaster, DepartmentMaster).join(BranchMaster,BranchMaster.code == UserMaster.branchcode).join(DesignationMaster,DesignationMaster.code == UserMaster.designationcode).join(DepartmentMaster,DepartmentMaster.code == UserMaster.departmentcode).all()
   usermaster = db.session.query(UserMaster, BranchMaster, DesignationMaster, DepartmentMaster).join(BranchMaster,BranchMaster.code == UserMaster.branchcode).join(DesignationMaster,DesignationMaster.code == UserMaster.designationcode).join(DepartmentMaster,DepartmentMaster.code == UserMaster.departmentcode).all()
   for det in details:
       print (det[0].user_level)
   user = format(current_user.Username)
   users=UserMaster.query.all()
   designations = DesignationMaster.query.all()
   branches = BranchMaster.query.all()
   departments = DepartmentMaster.query.all()
   form.username.data =''
   form.usercode.data =''
   return render_template('usermaster.html',form=form,users=users,branches=branches,departments=departments,designations=designations,details=details,user=user,usermaster=usermaster)

### INVOICE MASTER ###
class InvoiceMaster(db.Model):
   invoicecode = db.Column(db.Integer,primary_key=True)
   invoicename = db.Column(db.String(30))
   usercode = db.Column(db.String(30))
   usertype = db.Column(db.String(30))

class Invoiceform(FlaskForm):
   invoice_name =  StringField('Invoice Name', validators=[InputRequired()])

@app.route('/invoice',  methods = ['GET','POST'])
@login_required
def viewinvoice():
   try:
      form = Invoiceform()
      if form.validate_on_submit():
         new_invoice = InvoiceMaster(invoicename=form.invoice_name.data)
         db.session.add(new_invoice)
         db.session.commit()
         flash('Data added successfully')
   except IntegrityError:
      db.session.rollback()
      flash('Invoice already exists')
   invoices = InvoiceMaster.query.all()
   users = UserMaster.query.all()
   names = db.session.query(InvoiceMaster,UserMaster).join(UserMaster, InvoiceMaster.usercode == UserMaster.user_code).all()
   user = format(current_user.Username)
   print(invoices)
   print(names)
   form.invoice_name.data=''
   return render_template('/invoice.html', form=form,invoices=invoices,users=users,names=names,user=user)

### TAX MASTER ###

class TaxMaster(db.Model):
   taxcode = db.Column(db.Integer,primary_key=True)
   taxname = db.Column(db.String(30))
   taxpercent = db.Column(db.Float(8))

class Taxform(FlaskForm):
   tax_name = StringField('Tax Name', validators=[InputRequired()])
   tax_percentage = StringField('Tax Percentage', validators=[InputRequired()])

@app.route('/tax', methods = ['GET','POST'])
@login_required
def viewtax():
   try:
      form = Taxform()
      if form.validate_on_submit():
         new_tax = TaxMaster(taxname=form.tax_name.data,taxpercent=form.tax_percentage.data)
         db.session.add(new_tax)
         db.session.commit()
         flash('Data added successfully')
   except IntegrityError:
      db.session.rollback()
      flash('Tax already exists')
   user = format(current_user.Username)
   taxes = TaxMaster.query.all()
   form.tax_name.data=''
   form.tax_percentage.data=''
   return render_template('/tax.html', form=form,taxes=taxes,user=user)


###VENDOR MASTER###
class VendorMaster(db.Model):
   vendor_code    = db.Column(db.Integer, primary_key=True)
   vendor_name = db.Column(db.String(30), unique=True)
   vendor_city  = db.Column(db.String(30))
   vendor_state = db.Column(db.String(30))
   bank_name = db.Column(db.String(30))
   beneficiary_code = db.Column(db.String(30))
   beneficiary_name = db.Column(db.String(30))
   ifsc_code = db.Column(db.String(30))
   customer_ref_no = db.Column(db.String(30))
   pan_no = db.Column(db.String(30))
   invoice_code = db.Column(db.Integer)
   account_type = db.Column(db.Integer)

class Vendorform(FlaskForm):
    vendorname = StringField('Branch Name', validators=[InputRequired()])
    vendorcity = StringField('Branch City', validators=[InputRequired()])
    vendorstate = StringField('Branch State', validators=[InputRequired()])
    bankname = StringField('Bank Name')
    beneficiarycode = StringField('Beneficiary Code')
    beneficiaryname = StringField('Beneficiary Name')
    ifsccode = StringField('IFSC code')
    customerrefno = StringField('Customer Ref No')
    panno = StringField('Pan No')

@app.route('/vendor', methods=['GET', 'POST'])
@login_required
def viewvendor():
    try:
        form = Vendorform()
        vendors = VendorMaster.query.all()
        invoices = InvoiceMaster.query.all()
        invoice = request.form.get('invoice', None)
        print(invoice)
        vendorinvoicecode = db.session.query(InvoiceMaster.invoicecode).filter(
            InvoiceMaster.invoicename == invoice).scalar()
        if request.form.get('add_button'):
            my_string=form.vendorname.data
            print("vicky")
            str=my_string.split()  
            print(str)
            new_string=" ".join(str)
            print(new_string)
            new_vendor = VendorMaster(vendor_name=new_string, vendor_city=form.vendorcity.data,
                                      vendor_state=form.vendorstate.data, bank_name=form.bankname.data,
                                      beneficiary_code=form.beneficiarycode.data,
                                      beneficiary_name=form.beneficiaryname.data, ifsc_code=form.ifsccode.data,
                                      customer_ref_no=form.customerrefno.data, pan_no=form.panno.data,
                                      invoice_code=vendorinvoicecode)
            db.session.add(new_vendor)
            db.session.commit()
            flash('Data added successfully')
        if request.form.get('edit_button'):
            code = request.form.get('vendorcode')
            name = request.form.get('vendorname')
            city = request.form.get('vendorcity')
            bank = request.form.get('vendorbank')
            ben_name = request.form.get('beneficiary_name')
            ben_code = request.form.get('beneficiary_code')
            ifsc = request.form.get('ifsc_code')
            cust = request.form.get('customer_ref_no')
            pan = request.form.get('pan_no')
            update = VendorMaster.query.filter_by(vendor_code=code).update(
                {'vendor_name': request.form.get('vendorname'),
                 'vendor_city': request.form.get('vendorcity'),
                 'vendor_state': request.form.get('vendorstate'),
                 'bank_name': request.form.get('vendorbank'),
                 'beneficiary_name': request.form.get('beneficiary_name'),
                 'beneficiary_code': request.form.get('beneficiary_code'),
                 'ifsc_code': request.form.get('ifsc_code'),
                 'customer_ref_no': request.form.get('customer_ref_no'),
                 'pan_no': request.form.get('pan_no'),
                 'invoice_code': request.form.get('invoice')
                 })
            db.session.commit()
    except exc.IntegrityError as e:
        db.session().rollback()
        flash('Vendor already exists')
    user = format(current_user.Username)
    form.vendorname.data = ""
    form.vendorcity.data = ""
    form.vendorstate.data = ""
    form.bankname.data = ""
    form.beneficiarycode.data = ""
    form.beneficiaryname.data = ""
    form.customerrefno.data = ""
    form.ifsccode.data = ""
    form.panno.data = ""
    vendors = VendorMaster.query.all()
    invoices=InvoiceMaster.query.all()
    vend = db.session.query(VendorMaster,InvoiceMaster).join(InvoiceMaster,InvoiceMaster.invoicecode==VendorMaster.invoice_code).all()
    return render_template('vendor.html', form=form, vendors=vendors, user=user,invoices=invoices,vend=vend)

@app.route('/index_data')
def index_json():
    vendors = VendorMaster.query.all()
    payload = []
    content = {}
    for vendor in vendors:
        content = {'vendor_code': vendor.vendor_code, 'vendor_name': vendor.vendor_name,'vendor_city': vendor.vendor_city ,'bank_name': vendor.bank_name,'beneficiary_code': vendor.beneficiary_code,'beneficiary_name': vendor.beneficiary_name,'ifsc_code': vendor.ifsc_code,'customer_ref_no': vendor.customer_ref_no,'pan_no': vendor.pan_no,'vendor_state': vendor.vendor_state}
        payload.append(content)

    data ={"data":payload}
    print(data)
    return jsonify(data)

@app.route('/vendorinvoice',methods=['GET', 'POST'])
@login_required
def viewvendorinvoice():
    user = format(current_user.Username)
    vendors = VendorMaster.query.all()
    return render_template('vendorinvoice.html',user=user,vendors=vendors)

###PURCHASE NUMBER###
class PurchaseNumber(db.Model):
    Purchase_No = db.Column(db.Integer, primary_key=True,autoincrement = False)

###FLOW CONTROL MASTER###
class FlowControlMaster(db.Model):
    Purchase_No = db.Column(db.Integer, primary_key=True,autoincrement = False)
    Create_Date = db.Column(db.DateTime())
    Access_Date = db.Column(db.DateTime())
    Vendor_Code = db.Column(db.Integer)
    Total_Invalue = db.Column(db.Float(11, 2))
    From_User = db.Column(db.String(10))
    From_Branch = db.Column(db.Integer)
    To_User = db.Column(db.String(10))
    To_Branch = db.Column(db.Integer)
    User_Level = db.Column(db.Integer())
    Comments = db.Column(db.String(100))
    Flow_Flag = db.Column(db.String(1))
    Flag_Reject = db.Column(db.String(1))

###TRANSACTION MASTER###
class Transaction(db.Model):
    Purchase_No= db.Column(db.Integer, primary_key=True,autoincrement = False)
    Date =  db.Column(db.DateTime())
    User_code = db.Column(db.String(10))
    Branch_code = db.Column(db.Integer)
    Vendor_code = db.Column(db.Integer)
    Invoice_code = db.Column(db.Integer)
    Invoice_No = db.Column(db.String(20))
    Date = db.Column(db.DateTime())
    Purchase_Date = db.Column(db.Date())
    Purchase_Details = db.Column(db.String(100))
    Item_details = db.Column(db.String(200))
    Total_Value = db.Column(db.Float(6,2))
    Txn_code1 = db.Column(db.String(30))
    Txn_value1 = db.Column(db.Float(6,2))
    Txn_code2 = db.Column(db.String(30))
    Txn_value2 = db.Column(db.Float(6,2))
    Txn_code3 = db.Column(db.String(30))
    Txn_value3 = db.Column(db.Float(6,2))
    Total_Invalue = db.Column(db.Float(11,2))
    To_Usercode = db.Column(db.String(30))
    Attachment_docs = db.Column(db.String(100))
    User_comments  = db.Column(db.String(100))
    Auth_flag = db.Column(db.String(10))
    Payment_Type = db.Column(db.String(1))
    initiate_User_Code = db.Column(db.String(10))
    Quick_Flag = db.Column(db.String(1))
    Tds_Percentage = db.Column(db.Integer)
    Tds_Amount = db.Column(db.Integer)
    Total_Before_Value = db.Column(db.Float(11, 2))
    Utr_No = db.Column(db.String(250))
    Utr = db.Column(db.String(250))
    Mode = db.Column(db.String(15))


class Transactionform(FlaskForm):
    invoiceno = StringField('Invoice No')
    totalvalue = FloatField('Total Value')
    tdspercent = FloatField('Tds Percent')
    purdate = DateField('Entry Date',format='%Y-%m-%d',validators=(validators.Optional(),))
    image = FileField()
    utrnumber = FileField()
    fromdate = DateField('From Date', format='%Y-%m-%d')
    todate = DateField('To Date', format='%Y-%m-%d')

#### TRANSACT ONLY ####
@app.route('/transactlevel',methods=['GET', 'POST'])
@login_required
def viewtransactionlevel():
    form = Transactionform()
    user = format(current_user.Username)
    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()
    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,FlowControlMaster.Flow_Flag == "N",Transaction.Auth_flag == None).scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == None,Transaction.Auth_flag == None).scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).scalar()
    quickcounts_currentuser = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None,Transaction.To_Usercode == current_user_code).scalar()
    finish_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Auth_flag == "A").scalar()
    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    print(next_level_convert_int_to_string)
    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_convert_int_to_string).all()
    taxone = request.form.get('taxo', None)
    invoiceno =request.form.get('invoiceno',None)
    taxtwo = request.form.get('taxtw', None)
    taxthree = request.form.get('taxth', None)
    vendorname = request.form.get('vendorname', None)
    print(vendorname)
    invoicename = request.form.get('invoicename', None)
    branchname = request.form.get('branchname', None)
    purchasedate = form.purdate.data
    mode = request.form.get('mode', None)
    billdescription = request.form.get('bill', None)
    itemdescription = request.form.get('item', None)
    assignuser = request.form.get('assignto', None)
    comments = request.form.get('comment', None)
    payment = request.form.get('paytype', None)
    total_amount = form.totalvalue.data
    tds_percent = form.tdspercent.data
    print(assignuser)
    print(purchasedate)
    user = format(current_user.Username)
    purchasenum = db.session.query(PurchaseNumber.Purchase_No).scalar()
    print(purchasenum)
    if not tds_percent :
        tds_percent = 0
    try:
        form = Transactionform()
        if form.validate_on_submit():
            if vendorname is None:
                vendorname = 'NO VENDOR'
            if invoicename is None:
                invoicename = 'noinvoice'
            if branchname is None:
                branchname='nobranch'
            total_amount = form.totalvalue.data
            usercode = db.session.query(UserMaster.user_code).filter_by(user_code=current_user_code).first()
            fromuserbranch = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).first()
            branchcode = db.session.query(BranchMaster.code).filter_by(place=branchname).first()
            invoicecode = db.session.query(InvoiceMaster.invoicecode).filter_by(invoicename=invoicename).first()
            vendorcode = VendorMaster.query.with_entities(VendorMaster.vendor_code).filter_by(vendor_name=vendorname).scalar()
            print(vendorcode)
            tousercode = db.session.query(UserMaster.user_code).filter_by(Username=assignuser).first()
            touserbranch = db.session.query(UserMaster.branchcode).filter_by(Username=assignuser).first()
            touserlevel = db.session.query(UserMaster.user_level).filter_by(Username=assignuser).first()
            fromuserlevel = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).first()
            if form.image.data is None:
                image_url = ""
            else:
                image_filename = photos.save(form.image.data)
                image_url = photos.url(image_filename)
            purchaseno = db.session.query(PurchaseNumber.Purchase_No).scalar()
            new_transaction = Transaction(Purchase_No=purchasenum,Invoice_No=form.invoiceno.data,Total_Value=total_amount,Date = datetime.now(),Purchase_Date= form.purdate.data,Branch_code=branchcode,Vendor_code= vendorcode,Purchase_Details= billdescription,Item_details=itemdescription,Invoice_code= invoicecode,To_Usercode=tousercode,User_code=usercode,Total_Invalue=total_amount,Attachment_docs=image_url,Payment_Type=payment,initiate_User_Code=usercode,Total_Before_Value=form.totalvalue.data,Tds_Percentage=tds_percent,Tds_Amount=total_amount,Mode=mode)
            new_flow = FlowControlMaster(Purchase_No=purchasenum,Create_Date=datetime.now(),Access_Date=datetime.now(), Vendor_Code=vendorcode,Total_Invalue=total_amount,From_User=usercode,From_Branch=fromuserbranch,To_User=tousercode,To_Branch=touserbranch,User_Level=fromuserlevel,Comments=comments,Flow_Flag="N")
            db.session.add(new_transaction)
            db.session.add(new_flow)
            if request.form.get('check') == "Q":
                quickflag = Transaction.query.filter_by(Purchase_No=purchasenum).update({Transaction.Quick_Flag: "Q"})
            purchase = PurchaseNumber.query.filter_by(Purchase_No=purchasenum).update({PurchaseNumber.Purchase_No: purchasenum + 1})
            db.session.commit()
            flash('Data added successfully')
            date = datetime.now()
            return render_template('hello.html',purchasenum=purchasenum,purchasedate=purchasedate,invoicename=invoicename,invoiceno=invoiceno,tds_percent=tds_percent,tds_amount_value=total_amount,vendorname=vendorname,total_amount=total_amount,billdescription=billdescription,itemdescription=itemdescription,comments=comments,taxthree=taxthree,taxone=taxone,taxtwo=taxtwo,totalinvalue=total_amount,payment=payment,assignuser=assignuser,date=date,mode=mode)
    except exc.IntegrityError as e:
        db.session().rollback()
        flash('Invoice already exists')
    user = format(current_user.Username)
    invoices = InvoiceMaster.query.all()
    taxes = TaxMaster.query.all()
    users = UserMaster.query.all()
    branches = BranchMaster.query.all()
    vendors = VendorMaster.query.order_by(VendorMaster.vendor_name).all()
    form.invoiceno.data = ""
    form.totalvalue.data = ""
    form.purdate.data = ""
    return render_template('transactonly.html', form=form, user=user, invoices = invoices, taxes=taxes, users=users, branches=branches,vendors = vendors,purchasenum=purchasenum,user_levels=user_levels,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,quickcounts_currentuser=quickcounts_currentuser,finish_counts=finish_counts)

### VIEW ONLY ###
@app.route('/viewonly', methods=['GET','POST'])
def flow_controlonly():
    form = Transactionform()
    user = format(current_user.Username)
    current_user_code = format(current_user.user_code)
    reject_counts = db.session.query(func.count(FlowControlMaster.Flag_Reject)).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,FlowControlMaster.Flow_Flag == "N",Transaction.Auth_flag == None).scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == None,Transaction.Auth_flag == None).scalar()
    rej_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag == "N").scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).scalar()
    quickcounts_currentuser = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None,Transaction.To_Usercode == current_user_code).scalar()
    finish_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Auth_flag == "A").scalar()
    user_level = UserMaster.query.all()
    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_convert_int_to_string).all()
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    user_code = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    user_branch = db.session.query(BranchMaster.place).filter_by(code=user_code).scalar()
    ven_code = request.form.get('vendorname')
    vendor_name = db.session.query(VendorMaster.vendor_code).filter_by(vendor_name=ven_code).scalar()
    purno = request.form.get('purno')
    purchase_date = request.form.get('purchasedate')
    totalvalue = request.form.get('amount')
    to_user = request.form.get('user')
    user_comments = request.form.get('body')
    to_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(Username=to_user).scalar()
    to_user_code = db.session.query(UserMaster.user_code).filter_by(Username=to_user).scalar()
    to_userbranch = db.session.query(BranchMaster.place).filter_by(code=to_user_branchcode).scalar()
    if not user_levels:
        if request.method == "POST" and request.form.get('action'):
            purchase = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Auth_flag: "A"})
            flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update({FlowControlMaster.Flow_Flag: "Y"})
            flow = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date,Access_Date=datetime.now(), Vendor_Code=vendor_name, Total_Invalue=totalvalue,From_User=current_user_code, From_Branch=user_code, To_User=current_user_code,To_Branch=user_code, User_Level=from_user, Comments=user_comments, Flow_Flag = "Y")
            updatetransactfromuser=Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
            updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: current_user_code})
            db.session.add(flow)
            db.session.commit()
            if current_user.user_level == 5:
                if form.utrnumber.data is None:
                    utrno = ""
                else:
                    utr_filename = photos.save(form.utrnumber.data)
                    utrno = photos.url(utr_filename)
                updateutr = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Utr_No: utrno})
                db.session.commit()
            if current_user.user_level == 5:
                utrnumtext = request.form.get('utrnum')
                if utrnumtext is None:
                    utrnumtext = ""
                else:
                    utrnumtext = request.form.get('utrnum')
                updateutrnum = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Utr: utrnumtext})
                db.session.commit()
            return render_template('userlast.html', user=user, user_levels=user_levels, form=form,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,quickcounts_currentuser=quickcounts_currentuser,finish_counts=finish_counts,rej_counts=rej_counts)
    if request.method == "POST" and request.form.get('action'):
        flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno,To_User=current_user_code).update({FlowControlMaster.Flow_Flag: "Y"})
        flow_data = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date, Access_Date=datetime.now(),Vendor_Code=vendor_name, Total_Invalue=totalvalue, From_User=current_user_code,From_Branch=user_code, To_User=to_user_code, To_Branch=to_user_branchcode,User_Level=from_user, Comments=user_comments,Flow_Flag="N")
        updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
        updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: to_user_code})
        db.session.add(flow_data)
        db.session.commit()
        if current_user.user_level == 4:
            if form.utrnumber.data is None:
                utrno = ""
            else:
                utr_filename = photos.save(form.utrnumber.data)
                utrno = photos.url(utr_filename)
            updateutr = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Utr_No: utrno})
            db.session.commit()
        if current_user.user_level == 4:
            utrnumtext = request.form.get('utrnumbox')
            if utrnumtext is None:
                utrnumtext = ""
            else:
                utrnumtext = request.form.get('utrnumbox')
            updateutrnum = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Utr: utrnumtext})
            db.session.commit()
        return render_template('viewonly.html', user=user, user_levels=user_levels, form=form,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,finish_counts=finish_counts,rej_counts=rej_counts)
    from_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    to_user_code = db.session.query(UserMaster.user_code).filter_by(Username=to_user).scalar()
    return_user_code = db.session.query(FlowControlMaster.From_User.distinct()).filter_by(Purchase_No=purno,To_User=current_user_code,Flag_Reject=None).scalar()
    return_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(user_code=return_user_code).scalar()
    if not user_levels:
        if request.method == "POST" and request.form.get('act'):
            flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update({FlowControlMaster.Flow_Flag: "Y"})
            flow = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date,Access_Date=datetime.now(), Vendor_Code=vendor_name, Total_Invalue=totalvalue,From_User=current_user_code, From_Branch=from_user_branchcode,To_User=return_user_code,To_Branch=return_user_branchcode,User_Level=from_user, Comments=user_comments,Flow_Flag="N",Flag_Reject="R")
            updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
            updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: return_user_code})
            db.session.add(flow)
            db.session.commit()
        return render_template('userlast.html', user=user,user_levels=user_levels, form=form,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,finish_counts=finish_counts,rej_counts=rej_counts)
    if request.method == "POST" and request.form.get('act'):
        flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update({FlowControlMaster.Flow_Flag: "Y"})
        flow_data = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date, Access_Date=datetime.now(),Vendor_Code=vendor_name, Total_Invalue=totalvalue, From_User=current_user_code,From_Branch=from_user_branchcode,To_User=return_user_code,To_Branch=return_user_branchcode,User_Level=from_user, Comments=user_comments, Flow_Flag="N",Flag_Reject="R")
        updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
        updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: return_user_code})
        db.session.add(flow_data)
        db.session.commit()
        return render_template('viewonly.html', user=user, user_levels=user_levels, form=form,reject_counts=reject_counts, inbox_counts=inbox_counts, sent_counts=sent_counts,quick_counts=quick_counts, quickcounts_currentuser=quickcounts_currentuser,finish_counts=finish_counts,rej_counts=rej_counts)
    return render_template('viewonly.html', user=user, user_levels=user_levels, form=form,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,quickcounts_currentuser=quickcounts_currentuser,finish_counts=finish_counts,rej_counts=rej_counts)

@app.route('/flow')
def flow_jsondata():
    current_user_code = format(current_user.user_code)
    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.To_User == current_user_code,FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == None,Transaction.Auth_flag == None).all()
    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User,FlowControlMaster.Access_Date,BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == FlowControlMaster.From_User).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    payload = []
    content = {}
    for det in details:
        print(det)
        content = {'PaymentNo': det[1].Purchase_No, 'PaymentLevel': det[1].To_Usercode,
                   'RequestedOn': det[1].Date.strftime('%d-%m-%Y'),
                   'BranchName': det[2].place, 'VendorName': det[3].vendor_name,
                   'TotalValue': str('%0.2f' % det[1].Total_Invalue), 'PayMode': det[1].Mode,
                   'AttachmentCopy': det[1].Attachment_docs, 'BillDescription': det[1].Purchase_Details,
                   'ItemDescription': det[1].Item_details, 'PaymentType': det[1].Payment_Type,
                   'InvoiceFrom': det[5].Username, 'ifsccode': det[3].ifsc_code, 'bankname': det[3].bank_name,
                   'Invoicename': det[4].invoicename, 'Invoiceno': det[1].Invoice_No,
                   'PurchaseDate': det[1].Purchase_Date, 'comments': [],'UtrNo': det[1].Utr,'UtrAttach': det[1].Utr_No}
        for data in datas:
            if det[1].Purchase_No == data[0].Purchase_No:
                comment = {'comments': ['Message from %s on %s : %s' % (data[2], data[3].strftime('%d-%m-%Y %H:%M:%S'), data[1])]}
                schema = {
                "properties": {
                    "comments": {
                        "mergeStrategy": "append"
                        }
                    }
                }
                merger = Merger(schema)
                content = merger.merge(content, comment)

        payload.append(content)

    data = {"data": payload}
    print(data)
    return jsonify(data)





###REJECT ONLY####
@app.route('/rejectonly', methods=['GET', 'POST'])
def reject_controlonly():
    form = Transactionform()
    transaction = Transaction.query.all()
    users = UserMaster.query.all()
    branch = BranchMaster.query.all()
    vendor = VendorMaster.query.all()
    invoices = InvoiceMaster.query.all()
    level = UserMaster.query.all()
    taxes = TaxMaster.query.all()
    user = format(current_user.Username)
    current_user_code = format(current_user.user_code)
    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,FlowControlMaster.Flow_Flag == "N",Transaction.Auth_flag == None).scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == None,Transaction.Auth_flag == None).scalar()
    rej_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag == "N").scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).scalar()
    quickcounts_currentuser = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None,Transaction.To_Usercode == current_user_code).scalar()
    finish_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Auth_flag == "A").scalar()
    user_level = UserMaster.query.all()
    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_convert_int_to_string).all()
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    user_code = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    ven_code = request.form.get('vendorname')
    vendor_name = db.session.query(VendorMaster.vendor_code).filter_by(vendor_name=ven_code).scalar()
    purno = request.form.get('purno')
    purchase_date = request.form.get('purchasedate')
    totalvalue = request.form.get('amount')
    to_user = request.form.get('user')
    user_comments = request.form.get('body')
    create_date = db.session.query(Transaction.Date, FlowControlMaster).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).filter_by(Purchase_No=purno).scalar()
    to_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(Username=to_user).scalar()
    to_user_code = db.session.query(UserMaster.user_code).filter_by(Username=to_user).scalar()
    to_userbranch = db.session.query(BranchMaster.place).filter_by(code=to_user_branchcode).scalar()
    if not user_levels:
        if request.method == "POST" and request.form.get('action'):
            purchase = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Auth_flag: "A"})
            flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update({FlowControlMaster.Flow_Flag: "Y"})
            flow = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date,Access_Date=datetime.now(), Vendor_Code=vendor_name, Total_Invalue=totalvalue,From_User=current_user_code, From_Branch=user_code, To_User=current_user_code,To_Branch=to_user_branchcode, User_Level=from_user, Comments=user_comments, Flow_Flag = "Y")
            updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
            updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: current_user_code})
            db.session.add(flow)
            db.session.commit()
        return render_template('userlast.html',form=form,transaction=transaction,branch=branch,vendor=vendor,invoices=invoices,taxes=taxes,user=user,user_levels=user_levels,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,finish_counts=finish_counts,rej_counts=rej_counts)

    if request.method == "POST" and request.form.get('action'):
        flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update(
            {FlowControlMaster.Flow_Flag: "Y"})
        flow_data = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date, Access_Date=datetime.now(),
                                      Vendor_Code=vendor_name, Total_Invalue=totalvalue,
                                      From_User=current_user_code,
                                      From_Branch=user_code, To_User=to_user_code, To_Branch=to_user_branchcode,
                                      User_Level=from_user, Comments=user_comments, Flow_Flag="N")
        print(flow_data)
        updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update(
            {Transaction.User_code: current_user_code})
        updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update(
            {Transaction.To_Usercode: to_user_code})
        db.session.add(flow_data)
        db.session.commit()
        if current_user.user_level == 1:
            if form.image.data is None:
                image_url = ""
            else:
                image_filename = photos.save(form.image.data)
                image_url = photos.url(image_filename)
            invoiceno = request.form.get('invoiceno', None)
            invoicename = request.form.get('invoicename', None)
            invoicecode = db.session.query(InvoiceMaster.invoicecode).filter_by(invoicename=invoicename).first()
            vendorname = request.form.get('vendorname', None)
            vendorcode = db.session.query(VendorMaster.vendor_code).filter_by(vendor_name=vendorname).first()
            total_amount = request.form.get('amount', None)
            mode = request.form.get('paymode',None)
            print(type(total_amount))
            amount = float(total_amount)
            payment = request.form.get('paytype', None)
            # tds_percent = request.form.get('tds', None)
            # print(type(tds_percent))
            billdescription = request.form.get('bill', None)
            itemdescription = request.form.get('item', None)
            taxone = request.form.get('taxo', None)
            taxtwo = request.form.get('taxtw', None)
            taxthree = request.form.get('taxth', None)
            taxcodeone = db.session.query(TaxMaster.taxcode).filter_by(taxname=taxone).first()
            taxcodetwo = db.session.query(TaxMaster.taxcode).filter_by(taxname=taxtwo).first()
            taxcodethree = db.session.query(TaxMaster.taxcode).filter_by(taxname=taxthree).first()
            taxvalueone = db.session.query(TaxMaster.taxpercent).filter_by(taxname=taxone).scalar()
            taxvaluetwo = db.session.query(TaxMaster.taxpercent).filter_by(taxname=taxtwo).scalar()
            taxvaluethree = db.session.query(TaxMaster.taxpercent).filter_by(taxname=taxthree).scalar()
            if taxvalueone is None:
                taxvalueone = 0
            if taxvaluetwo is None:
                taxvaluetwo = 0
            if taxvaluethree is None:
                taxvaluethree = 0
            # tds = float(tds_percent)
            # print(tds)
            # tds_amount_value = tds / 100 * amount
            # tds_total_value = amount - tds_amount_value
            # txnamount1 = tds_total_value / 100 * taxvalueone
            # txnamount2 = tds_total_value / 100 * taxvaluetwo
            # txnamount3 = tds_total_value / 100 * taxvaluethree
            # totalinvalue = tds_total_value + txnamount1 + txnamount2 + txnamount3
            updatemode = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Mode: mode})
            updateimage = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Attachment_docs: image_url})
            updateinvoiceno = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Invoice_No: invoiceno})
            updateinvoicename = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Invoice_code: invoicecode})
            updatevendorname = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Vendor_code: vendorcode})
            updateamount = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Total_Before_Value: total_amount})
            updatepaytype = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Payment_Type: payment})
            # updatetds = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Tds_Percentage: tds_percent})
            updatebill = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Purchase_Details: billdescription})
            updateitem = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Item_details: itemdescription})
            updatetcode1 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_code1: taxcodeone})
            updatetcode2 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_code2: taxcodetwo})
            updatetcode3 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_code3: taxcodethree})
            # updatetvalue1 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_value1: txnamount1})
            # updatetvalue2 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_value2: txnamount2})
            # updatetvalue3 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_value3: txnamount3})
            # totalinvalue = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Total_Invalue: totalinvalue})
            totalval = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Total_Value: total_amount})
            db.session.commit()
            return render_template('rejectonly.html',form=form,transaction=transaction,branch=branch,vendor=vendor,invoices=invoices,taxes=taxes,user=user,user_levels=user_levels,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,finish_counts=finish_counts,rej_counts=rej_counts)
        if current_user.user_level == 4:
            if form.utrnumber.data is None:
                utrno = ""
            else:
                utr_filename = photos.save(form.utrnumber.data)
                utrno = photos.url(utr_filename)
                updateutr = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Utr_No: utrno})
                db.session.commit()
        if current_user.user_level == 4:
            utrnumtext = request.form.get('utrnumbox')
            if utrnumtext is None:
                utrnumtext = ""
            else:
                utrnumtext = request.form.get('utrnumbox')
                updateutrnum = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Utr: utrnumtext})
                db.session.commit()
        return render_template('rejectonly.html',form=form,transaction=transaction,branch=branch,vendor=vendor,invoices=invoices,taxes=taxes,user=user,user_levels=user_levels,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,finish_counts=finish_counts,rej_counts=rej_counts)

    from_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    to_user_code = db.session.query(UserMaster.user_code).filter_by(Username=to_user).scalar()
    return_user_code = db.session.query(FlowControlMaster.From_User.distinct()).filter_by(Purchase_No=purno,To_User=current_user_code,Flag_Reject=None).scalar()
    print(return_user_code)
    return_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(user_code=return_user_code).scalar()
    if not user_levels:
        if request.method == "POST" and request.form.get('act'):
            flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update({FlowControlMaster.Flow_Flag: "Y"})
            flow = FlowControlMaster(Purchase_No=purno, Create_Date=create_date,Access_Date=datetime.now(), Vendor_Code=vendor_name, Total_Invalue=totalvalue,From_User=current_user_code, From_Branch=from_user_branchcode,To_User=return_user_code, To_Branch=return_user_branchcode,User_Level=from_user, Comments=user_comments,Flow_Flag="N", Flag_Reject="R")
            # flagreject = FlowControlMaster.query.filter_by(Purchase_No=purno, From_User=current_user_code, To_User=return_user_code).update({FlowControlMaster.Flag_Reject: "R"})
            updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
            updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: return_user_code})
            db.session.add(flow)
            db.session.commit()
        return render_template('userlast.html',form=form,transaction=transaction,branch=branch,vendor=vendor,invoices=invoices,taxes=taxes,user=user,user_levels=user_levels,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,finish_counts=finish_counts,rej_counts=rej_counts)
    if request.method == "POST" and request.form.get('act'):
        flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update({FlowControlMaster.Flow_Flag: "Y"})
        flow_data = FlowControlMaster(Purchase_No=purno, Create_Date=create_date, Access_Date=datetime.now(),Vendor_Code=vendor_name, Total_Invalue=totalvalue, From_User=current_user_code,From_Branch=from_user_branchcode, To_User=return_user_code,To_Branch=return_user_branchcode,User_Level=from_user, Comments=user_comments, Flow_Flag="N", Flag_Reject="R")
        updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
        updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: return_user_code})
        db.session.add(flow_data)
        db.session.commit()
        return render_template('rejectonly.html',form=form,transaction=transaction,branch=branch,vendor=vendor,invoices=invoices,taxes=taxes,user=user,user_levels=user_levels,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,finish_counts=finish_counts,rej_counts=rej_counts)

    return render_template('rejectonly.html',form=form,transaction=transaction,branch=branch,vendor=vendor,invoices=invoices,taxes=taxes,user=user,user_levels=user_levels,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,finish_counts=finish_counts,rej_counts=rej_counts)

@app.route('/rejbyothers')
def rejbyothers_jsondata():
    current_user_code = format(current_user.user_code)
    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.To_User == current_user_code,FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == "R").all()
    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User,FlowControlMaster.Access_Date, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    payload = []
    content = {}
    for det in details:
        print(det)
        content = {'PaymentNo': det[1].Purchase_No, 'PaymentLevel': det[1].To_Usercode,
                   'RequestedOn': det[1].Date.strftime('%d-%m-%Y'),
                   'BranchName': det[2].place, 'VendorName': det[3].vendor_name,
                   'TotalValue': str('%0.2f' % det[1].Total_Invalue), 'PayMode': det[1].Mode,
                   'AttachmentCopy': det[1].Attachment_docs, 'BillDescription': det[1].Purchase_Details,
                   'ItemDescription': det[1].Item_details, 'PaymentType': det[1].Payment_Type,
                   'InvoiceFrom': det[5].Username, 'ifsccode': det[3].ifsc_code, 'bankname': det[3].bank_name,
                   'Invoicename': det[4].invoicename, 'Invoiceno': det[1].Invoice_No,
                   'PurchaseDate': det[1].Purchase_Date, 'comments': [],'UtrNo': det[1].Utr,'UtrAttach': det[1].Utr_No,'Quick_Flag': det[1].Quick_Flag}
        for data in datas:
            if det[1].Purchase_No == data[0].Purchase_No:
                comment = {'comments': ['Message from %s on %s : %s' % (data[2], data[3].strftime('%d-%m-%Y %H:%M:%S'), data[1])]}
                schema = {
                "properties": {
                    "comments": {
                        "mergeStrategy": "append"
                        }
                    }
                }
                merger = Merger(schema)
                content = merger.merge(content, comment)

        payload.append(content)

    data = {"data": payload}
    print(data)
    return jsonify(data)


@app.route('/sentonly', methods=['GET','POST'])
def sent_controlonly():
    current_user_code = format(current_user.user_code)
    users = UserMaster.query.all()
    branch = BranchMaster.query.all()
    vendor = VendorMaster.query.all()
    invoices = InvoiceMaster.query.all()
    level = UserMaster.query.all()
    user = format(current_user.Username)
    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,FlowControlMaster.Flow_Flag == "N",Transaction.Auth_flag == None).scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == None,Transaction.Auth_flag == None).scalar()
    rej_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag == "N").scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()
    quickcounts_currentuser = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None,Transaction.To_Usercode == current_user_code).scalar()
    finish_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Auth_flag == "A").scalar()
    sentto = db.session.query(Transaction,FlowControlMaster,UserMaster).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join(UserMaster,UserMaster.user_code == FlowControlMaster.To_User).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == None).all()
    time = db.session.query(FlowControlMaster.From_User, FlowControlMaster.Access_Date, Transaction, UserMaster.Username).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(UserMaster,UserMaster.user_code==FlowControlMaster.From_User)
    return render_template('sentonly.html',user=user,branch=branch, vendor=vendor,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,quickcounts_currentuser=quickcounts_currentuser,finish_counts=finish_counts,time=time,sentto=sentto,rej_counts=rej_counts)

@app.route('/sent')
def sent_json():
    current_user_code = format(current_user.user_code)
    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == FlowControlMaster.To_User).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == None,Transaction.Auth_flag == None).all()
    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User,FlowControlMaster.Access_Date, BranchMaster, VendorMaster, InvoiceMaster,UserMaster.Username).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == FlowControlMaster.From_User).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    payload = []
    content = {}
    for det in details:
        content = {'PaymentNo': det[1].Purchase_No, 'PaymentLevel': det[1].To_Usercode,
                   'RequestedOn': det[1].Date.strftime('%d-%m-%Y'),
                   'BranchName': det[2].place, 'VendorName': det[3].vendor_name,
                   'TotalValue': str('%0.2f' % det[1].Total_Invalue), 'PayMode': det[1].Mode,
                   'AttachmentCopy': det[1].Attachment_docs, 'BillDescription': det[1].Purchase_Details,
                   'ItemDescription': det[1].Item_details, 'PaymentType': det[1].Payment_Type,
                   'InvoiceTo': det[5].Username, 'ifsccode': det[3].ifsc_code, 'bankname': det[3].bank_name,
                   'Invoicename': det[4].invoicename, 'Invoiceno': det[1].Invoice_No,
                   'PurchaseDate': det[1].Purchase_Date, 'comments': [], 'UtrNo': det[1].Utr,
                   'UtrAttach': det[1].Utr_No}
        for data in datas:
            if det[1].Purchase_No == data[0].Purchase_No:
                comment = {'comments': ['Message from %s on %s : %s' % (data[2], data[3].strftime('%d-%m-%Y %H:%M:%S'), data[1])]}
                schema = {
                  "properties": {
                   "comments": {
                    "mergeStrategy": "append"
                    }
                }
            }
                merger = Merger(schema)
                content = merger.merge(content,comment)

        payload.append(content)

    data ={"data":payload}
    print(data)
    return jsonify(data)



@app.route('/rejectbyme', methods=['GET', 'POST'])
def rejbyme_controlonly():
    transact = Transactionform()
    transaction = Transaction.query.all()
    users = UserMaster.query.all()
    branch = BranchMaster.query.all()
    vendor = VendorMaster.query.all()
    invoices = InvoiceMaster.query.all()
    level = UserMaster.query.all()
    user = format(current_user.Username)
    current_user_code = format(current_user.user_code)
    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()
    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_add).all()
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,FlowControlMaster.Flow_Flag == "N",Transaction.Auth_flag == None).scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == None,Transaction.Auth_flag == None).scalar()
    rej_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag == "N").scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()
    quickcounts_currentuser = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None,Transaction.To_Usercode == current_user_code).scalar()
    finish_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Auth_flag == "A").scalar()
    user_code = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    user_branch = db.session.query(BranchMaster.place).filter_by(code=user_code).scalar()
    ven_code = request.form.get('vendorname')
    to_user = request.form.get('user')
    to_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(Username=to_user).scalar()
    return render_template('rejectbyme.html', user=user, transaction=transaction, branch=branch, vendor=vendor,user_levels=user_levels,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,transact=transact,quickcounts_currentuser=quickcounts_currentuser,finish_counts=finish_counts,rej_counts=rej_counts)

@app.route('/rejbyme')
def rejbyme_jsondata():
    current_user_code = format(current_user.user_code)
    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == FlowControlMaster.To_User).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag == "N").all()
    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User,FlowControlMaster.Access_Date, BranchMaster, VendorMaster, InvoiceMaster,UserMaster.Username).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == FlowControlMaster.From_User).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    payload = []
    content = {}
    for det in details:
        print(det)
        content = {'PaymentNo': det[1].Purchase_No, 'PaymentLevel': det[1].To_Usercode,
                   'RequestedOn': det[1].Date.strftime('%d-%m-%Y'),
                   'BranchName': det[2].place, 'VendorName': det[3].vendor_name,
                   'TotalValue': str('%0.2f' % det[1].Total_Invalue), 'PayMode': det[1].Mode,
                   'AttachmentCopy': det[1].Attachment_docs, 'BillDescription': det[1].Purchase_Details,
                   'ItemDescription': det[1].Item_details, 'PaymentType': det[1].Payment_Type,
                   'InvoiceTo': det[5].Username, 'ifsccode': det[3].ifsc_code, 'bankname': det[3].bank_name,
                   'Invoicename': det[4].invoicename, 'Invoiceno': det[1].Invoice_No,
                   'PurchaseDate': det[1].Purchase_Date, 'comments': [],'UtrNo': det[1].Utr,'UtrAttach': det[1].Utr_No,'Quick_Flag': det[1].Quick_Flag,'SentBy':current_user.Username}
        for data in datas:
            if det[1].Purchase_No == data[0].Purchase_No:
                comment = {'comments': ['Message from %s on %s : %s' % (data[2], data[3].strftime('%d-%m-%Y %H:%M:%S'), data[1])]}
                schema = {
                "properties": {
                    "comments": {
                        "mergeStrategy": "append"
                        }
                    }
                }
                merger = Merger(schema)
                content = merger.merge(content, comment)

        payload.append(content)

    data = {"data": payload}
    return jsonify(data)


@app.route('/quickonly',methods=['GET', 'POST'])
def quick_controlonly():
    form = Transactionform()
    transaction = Transaction.query.all()
    users = UserMaster.query.all()
    branch = BranchMaster.query.all()
    vendor = VendorMaster.query.all()
    invoices = InvoiceMaster.query.all()
    level = UserMaster.query.all()
    user = format(current_user.Username)
    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()
    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_add).all()
    print('user_levels is',user_level)
    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R", FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,FlowControlMaster.Flow_Flag == "N",Transaction.Auth_flag == None).scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == None,Transaction.Auth_flag == None).scalar()
    rej_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag == "N").scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).scalar()
    quickcounts_currentuser = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None,Transaction.To_Usercode == current_user_code).scalar()
    finish_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Auth_flag == "A").scalar()
    return render_template('quickonly.html', user=user, transaction=transaction, branch=branch, vendor=vendor,user_levels=user_levels, form=form,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,quickcounts_currentuser=quickcounts_currentuser,finish_counts=finish_counts,rej_counts=rej_counts)

@app.route('/quick_data')
def quick_json():
    current_user_code = format(current_user.user_code)
    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).all()
    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User,FlowControlMaster.Access_Date, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == FlowControlMaster.From_User).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    payload = []
    content = {}
    for det in details:
        print(det)
        content = {'PaymentNo': det[1].Purchase_No, 'PaymentLevel': det[1].To_Usercode,
                   'RequestedOn': det[1].Date.strftime('%d-%m-%Y'),
                   'BranchName': det[2].place, 'VendorName': det[3].vendor_name,
                   'TotalValue': str('%0.2f' % det[1].Total_Invalue), 'PayMode': det[1].Mode,
                   'AttachmentCopy': det[1].Attachment_docs, 'BillDescription': det[1].Purchase_Details,
                   'ItemDescription': det[1].Item_details, 'PaymentType': det[1].Payment_Type,
                   'InvoiceFrom': det[5].Username, 'ifsccode': det[3].ifsc_code, 'bankname': det[3].bank_name,
                   'Invoicename': det[4].invoicename, 'Invoiceno': det[1].Invoice_No,
                   'PurchaseDate': det[1].Purchase_Date, 'comments': [], 'UtrNo': det[1].Utr,
                   'UtrAttach': det[1].Utr_No}
        for data in datas:
            if det[1].Purchase_No == data[0].Purchase_No:
                comment = {'comments': [
                    'Message from %s on %s : %s' % (data[2], data[3].strftime('%d-%m-%Y %H:%M:%S'), data[1])]}
                schema = {
                    "properties": {
                        "comments": {
                            "mergeStrategy": "append"
                        }
                    }
                }
                merger = Merger(schema)
                content = merger.merge(content, comment)

        payload.append(content)

    data = {"data": payload}
    print(data)
    return jsonify(data)


@app.route("/export", methods=['GET'])
def export():
    current_user_code = format(current_user.user_code)
    print(current_user_code)
    query_sets = db.session.query(VendorMaster.customer_ref_no,VendorMaster.vendor_name,VendorMaster.beneficiary_code,VendorMaster.ifsc_code,VendorMaster.account_type,FlowControlMaster.Total_Invalue,FlowControlMaster.Access_Date).join(VendorMaster,VendorMaster.vendor_code==FlowControlMaster.Vendor_Code).distinct(FlowControlMaster.Purchase_No).filter(FlowControlMaster.From_User==current_user_code).all()
    column_names = ['customer_ref_no','vendor_name','beneficiary_code','ifsc_code','account_type','Total_Invalue','Access_Date']
    num = [set for set in query_sets]
    return excel.make_response_from_query_sets(query_sets,column_names,"xls")

@app.route('/invoicestatus', methods=['GET', 'POST'])
def status_controlonly():
    form = Transactionform()
    transaction = Transaction.query.all()
    users = UserMaster.query.all()
    branch = BranchMaster.query.all()
    vendor = VendorMaster.query.all()
    invoices = InvoiceMaster.query.all()
    level = UserMaster.query.all()
    user = format(current_user.Username)
    current_user_code = format(current_user.user_code)
    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()
    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_add).all()
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R", FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,FlowControlMaster.Flow_Flag == "N",Transaction.Auth_flag == None).scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == None,Transaction.Auth_flag == None).scalar()
    rej_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag == "N").scalar()
    finish_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Auth_flag == "A").scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).scalar()
    quickcounts_currentuser = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None,Transaction.To_Usercode == current_user_code).scalar()
    return render_template('authenticated.html', user=user, transaction=transaction, branch=branch, vendor=vendor,user_levels=user_levels, form=form,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,quickcounts_currentuser=quickcounts_currentuser,finish_counts=finish_counts,rej_counts=rej_counts)

@app.route('/payment_done')
def payment_json():
    details = details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.initiate_User_Code).filter(Transaction.Auth_flag == "A").all()
    datas = db.session.query(Transaction,FlowControlMaster.Comments,FlowControlMaster.From_User,FlowControlMaster.Access_Date, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    payload = []
    content = {}
    for det in details:
        content = {'PaymentNo': det[1].Purchase_No, 'PaymentLevel': det[1].To_Usercode,'RequestedOn': det[1].Date.strftime('%d-%m-%Y') ,'PaymentType': det[4].invoicename,'BranchName': det[2].place,'VendorName': det[3].vendor_name,'TotalValue': str('%0.2f' % det[1].Total_Invalue),'PayMode': det[1].Mode,'AttachmentCopy': det[1].Attachment_docs,'BillDescription': det[1].Purchase_Details,'ItemDescription': det[1].Item_details,'PaymentType': det[1].Payment_Type,'InvoiceFrom': det[5].Username,'ifsccode': det[3].ifsc_code,'bankname': det[3].bank_name,'Invoicename': det[4].invoicename,'Invoiceno': det[1].Invoice_No,'PurchaseDate': det[1].Purchase_Date,'comments': []}
        for data in datas:
            if det[1].Purchase_No == data[0].Purchase_No:
                comment = {'comments': ['Message from %s on %s : %s' % (data[2], data[3].strftime('%d-%m-%Y %H:%M:%S'), data[1])]}
                schema = {
                  "properties": {
                   "comments": {
                    "mergeStrategy": "append"
                    }
                }
            }
                merger = Merger(schema)
                content = merger.merge(content,comment)

        payload.append(content)

    data ={"data":payload}
    print(data)
    return jsonify(data)


@app.route('/alltransaction', methods=['GET', 'POST'])
def all_controlonly():
    transact = Transactionform()
    transaction = Transaction.query.all()
    users = UserMaster.query.all()
    branch = BranchMaster.query.all()
    vendor = VendorMaster.query.all()
    invoices = InvoiceMaster.query.all()
    level = UserMaster.query.all()
    user = format(current_user.Username)
    print(user)
    current_user_code = format(current_user.user_code)
    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).all()
    print(current_user_code)
    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()
    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_add).all()
    print('user_levels is',user_level)
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    print(from_user)
    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,FlowControlMaster.Flow_Flag == "N",Transaction.Auth_flag == None).scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == None,Transaction.Auth_flag == None).scalar()
    rej_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag == "N").scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()
    quickcounts_currentuser = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None,Transaction.To_Usercode == current_user_code).scalar()
    finish_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Auth_flag == "A").scalar()
    user_code = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    user_branch = db.session.query(BranchMaster.place).filter_by(code=user_code).scalar()
    ven_code = request.form.get('vendorname')
    vendor_name = db.session.query(VendorMaster.vendor_code).filter_by(vendor_name=ven_code).scalar()
    purno = request.form.get('purno')
    yo_user = current_user_code
    purchase_date = request.form.get('purchasedate')
    totalvalue = request.form.get('amount')
    to_user = request.form.get('user')
    user_comments = request.form.get('body')
    to_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(Username=to_user).scalar()
    to_user_code = db.session.query(UserMaster.user_code).filter_by(Username=to_user).scalar()
    to_userbranch = db.session.query(BranchMaster.place).filter_by(code=to_user_branchcode).scalar()
    invoicelevel = db.session.query(Transaction,UserMaster).join(UserMaster,UserMaster.user_code == Transaction.To_Usercode).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).all()
    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User,FlowControlMaster.Access_Date, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    return render_template('alltransaction.html', user=user, transaction=transaction, branch=branch, vendor=vendor,details=details, user_levels=user_levels,datas=datas,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,transact=transact,quickcounts_currentuser=quickcounts_currentuser,finish_counts=finish_counts,invoicelevel=invoicelevel,rej_counts=rej_counts)

@app.route('/password',methods=['GET','POST'])
@login_required
def password():
    user = format(current_user.Username)
    current_user_code = format(current_user.user_code)
    if request.method == 'POST':
        currpass = request.form['currpass']
        password = request.form['password']
        confirmpassword = request.form['confirmpass']
        if current_user.Password != currpass:
            flash('Current Password Is Wrong')
        if current_user.Password == currpass:
            if password == confirmpassword:
                print(confirmpassword)
                updatepass = UserMaster.query.filter_by(user_code=current_user_code).update({UserMaster.Password: confirmpassword})
                db.session.commit()
                flash('Password Updated Successfully')
            else:
                flash('Passwords Do Not Match')
    return render_template('password.html',user=user)

@app.route('/exp', methods=['GET', 'POST'])
def exp():
    transact = Transactionform()
    transaction = Transaction.query.all()
    branch = BranchMaster.query.all()
    vendor = VendorMaster.query.all()
    user = format(current_user.Username)
    print(user)
    current_user_code = format(current_user.user_code)
    print(current_user_code)
    current_user_code = format(current_user.user_code)
    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_add).all()
    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,FlowControlMaster.Flow_Flag == "N",Transaction.Auth_flag == None).scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct()),Transaction).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).filter(FlowControlMaster.From_User == current_user_code,FlowControlMaster.Flag_Reject == None,Transaction.Auth_flag == None).scalar()
    rej_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == "R",FlowControlMaster.Flow_Flag == "N").scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()
    quickcounts_currentuser = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None,Transaction.To_Usercode == current_user_code).scalar()
    finish_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Auth_flag == "A").scalar()
    return render_template('exportdata.html', user=user, transaction=transaction, branch=branch, vendor=vendor,user_levels=user_levels,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,transact=transact,quickcounts_currentuser=quickcounts_currentuser,finish_counts=finish_counts,rej_counts=rej_counts)

@app.route('/export_data')
def export_json():
    current_user_code = format(current_user.user_code)
    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,VendorMaster.vendor_code == Transaction.Vendor_code).join(InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == None).all()
    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User,FlowControlMaster.Access_Date, BranchMaster, VendorMaster, InvoiceMaster,UserMaster.Username).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == FlowControlMaster.From_User).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    payload = []
    content = {}
    for det in details:
        content = {'PaymentNo': det[1].Purchase_No, 'PaymentLevel': det[1].To_Usercode,
                   'RequestedOn': det[1].Date.strftime('%d-%m-%Y'),
                   'BranchName': det[2].place, 'VendorName': det[3].vendor_name,
                   'TotalValue': str('%0.2f' % det[1].Total_Invalue), 'PayMode': det[1].Mode,
                   'AttachmentCopy': det[1].Attachment_docs, 'BillDescription': det[1].Purchase_Details,
                   'ItemDescription': det[1].Item_details, 'PaymentType': det[1].Payment_Type,
                   'InvoiceTo': det[5].Username, 'ifsccode': det[3].ifsc_code, 'bankname': det[3].bank_name,
                   'Invoicename': det[4].invoicename, 'Invoiceno': det[1].Invoice_No,
                   'PurchaseDate': det[1].Purchase_Date, 'comments': [], 'UtrNo': det[1].Utr,
                   'UtrAttach': det[1].Utr_No,'Customer_Ref_No':det[3].customer_ref_no,'Beneficiary_Code':det[3].beneficiary_code,'Account_Type':det[3].account_type,'Value_Date':det[1].Date}
        for data in datas:
            if det[1].Purchase_No == data[0].Purchase_No:
                comment = {'comments': ['Message from %s on %s : %s' % (data[2], data[3].strftime('%d-%m-%Y %H:%M:%S'), data[1])]}
                schema = {
                  "properties": {
                   "comments": {
                    "mergeStrategy": "append"
                    }
                }
            }
                merger = Merger(schema)
                content = merger.merge(content,comment)

        payload.append(content)

    data ={"data":payload}
    print(data)
    return jsonify(data)






@app.route('/beats', methods=['GET', 'POST'])
def beats():
    return render_template('beatsslideshow.html')


if __name__ == '__main__':
    excel.init_excel(app)
    app.run(debug=False,host='192.168.1.194',port=5000)
