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
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField,DateField,IntegerField,FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from wtforms.fields.html5 import DateField
from flask_uploads import UploadSet, configure_uploads, IMAGES , ALL
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy import func,cast,DATE
import cgi

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

   def __repr__(self):
      return '{}'.format(self.place)
def BranchMaster_query():
    return BranchMaster.query


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
   for det in details:
       print (det[0].user_level)

   user = format(current_user.Username)
   users=UserMaster.query.all()
   designations = DesignationMaster.query.all()
   branches = BranchMaster.query.all()
   departments = DepartmentMaster.query.all()
   form.username.data =''
   form.usercode.data =''


   return render_template('usermaster.html',form=form,users=users,branches=branches,departments=departments,designations=designations,details=details,user=user)

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

   def __repr__(self):
      return '{}'.format(self.place)
def VendorMaster_query():
    return VendorMaster.query


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
        edit = request.form.get('edit_button')
        code = request.form.get('vendorcode')
        print(code)
        print(edit)
        if form.validate_on_submit():
            if request.form.get('add_button') == 'add':
                new_vendor = VendorMaster(vendor_name=form.vendorname.data, vendor_city=form.vendorcity.data,
                                          vendor_state=form.vendorstate.data, bank_name=form.bankname.data,
                                          beneficiary_code=form.beneficiarycode.data,
                                          beneficiary_name=form.beneficiaryname.data, ifsc_code=form.ifsccode.data,
                                          customer_ref_no=form.customerrefno.data, pan_no=form.panno.data)

                db.session.add(new_vendor)
                db.session.commit()
                flash('Data added successfully')
            if request.form.get('edit_button') == 'edit':
                code = request.form.get('vendorcode')
                name = request.form.get('vendorname')
                city = request.form.get('vendorcity')
                bank = request.form.get('vendorbank')
                ben_name = request.form.get('beneficiary_name')
                ben_code = request.form.get('beneficiary_code')
                ifsc = request.form.get('ifsc_code')
                cust = request.form.get('customer_ref_no')
                pan = request.form.get('pan_no')
                print(code)
                print(name)
                print(city)
                print(bank)
                print(ben_name)
                print(ben_code)
                print(ifsc)
                print(cust)
                print(pan)
                update = VendorMaster.query.filter_by(vendor_code=code).update(
                    {'vendor_name': request.form.get('vendorname'),
                     'vendor_city': request.form.get('vendorcity'),
                     'vendor_state': request.form.get('vendorstate'),
                     'bank_name': request.form.get('vendorbank'),
                     'beneficiary_name': request.form.get('beneficiary_name'),
                     'beneficiary_code': request.form.get('beneficiary_code'),
                     'ifsc_code': request.form.get('ifsc_code'),
                     'customer_ref_no': request.form.get('customer_ref_no'),
                     'pan_no': request.form.get('pan_no')
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
    return render_template('vendor.html', form=form, vendors=vendors, user=user)

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


class Transactionform(FlaskForm):
    invoiceno = StringField('Invoice No', validators=[InputRequired()])
    totalvalue = FloatField('Total Value',validators = [InputRequired()])
    tdspercent = FloatField('Tds Percent')
    purdate = DateField('Entry Date',format='%Y-%m-%d',validators=[InputRequired()])
    image = FileField(validators=[InputRequired()])
    fromdate = DateField('From Date', format='%Y-%m-%d')
    todate = DateField('To Date', format='%Y-%m-%d')

class Viewform(FlaskForm):
    fromdate = DateField('From Date',format='%Y-%m-%d')
    todate = DateField('To Date',format='%Y-%m-%d')

@app.route('/transact',methods=['GET', 'POST'])
@login_required
def viewtransaction():
    form = Transactionform()
    user = format(current_user.Username)
    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()

    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    print(next_level)
    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    print(next_level_convert_int_to_string)

    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_convert_int_to_string).all()
    print(user_levels)
    taxone = request.form.get('taxo', None)
    print(taxone)
    taxtwo = request.form.get('taxtw', None)
    taxthree = request.form.get('taxth', None)
    vendorname = request.form.get('vendorname', None)
    invoicename = request.form.get('invoicename', None)
    branchname = request.form.get('branchname', None)
    purchasedate = request.form.get('purchasedate', None)
    billdescription = request.form.get('bill', None)
    itemdescription = request.form.get('item', None)
    assignuser = request.form.get('assignto', None)
    comments = request.form.get('comment', None)
    payment = request.form.get('paytype', None)
    total_amount = form.totalvalue.data
    print(assignuser)
    print(purchasedate)
    user = format(current_user.Username)
    purchasenum = db.session.query(PurchaseNumber.Purchase_No).scalar()
    print(purchasenum)
    purchase = PurchaseNumber.query.filter_by(Purchase_No=purchasenum).update(
        {PurchaseNumber.Purchase_No: purchasenum + 1})
    db.session.commit()
    quickflag = request.form.get('check',None)
    print(quickflag)


    #tax_val2 = [value for value in taxvaluetwo]
    #tax_val3 = [value for value in taxvaluethree]
    #amount = total_amount




    try:
        form = Transactionform()
        if form.validate_on_submit():
            total_amount = form.totalvalue.data
            usercode = db.session.query(UserMaster.user_code).filter_by(user_code=current_user_code).first()
            fromuserbranch = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).first()
            taxcodeone = db.session.query(TaxMaster.taxcode).filter_by(taxname=taxone).first()
            taxcodetwo = db.session.query(TaxMaster.taxcode).filter_by(taxname=taxtwo).first()
            taxcodethree = db.session.query(TaxMaster.taxcode).filter_by(taxname=taxthree).first()
            taxvalueone = db.session.query(TaxMaster.taxpercent).filter_by(taxname=taxone).scalar()
            taxvaluetwo = db.session.query(TaxMaster.taxpercent).filter_by(taxname=taxtwo).scalar()
            taxvaluethree = db.session.query(TaxMaster.taxpercent).filter_by(taxname=taxthree).scalar()
            branchcode = db.session.query(BranchMaster.code).filter_by(place=branchname).first()
            invoicecode = db.session.query(InvoiceMaster.invoicecode).filter_by(invoicename=invoicename).first()
            vendorcode = db.session.query(VendorMaster.vendor_code).filter_by(vendor_name=vendorname).first()
            tousercode = db.session.query(UserMaster.user_code).filter_by(Username=assignuser).first()
            touserbranch = db.session.query(UserMaster.branchcode).filter_by(Username=assignuser).first()
            touserlevel = db.session.query(UserMaster.user_level).filter_by(Username=assignuser).first()
            fromuserlevel = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).first()
            image_filename = photos.save(form.image.data)
            image_url = photos.url(image_filename)

            purchaseno = db.session.query(PurchaseNumber.Purchase_No).scalar()
            print(purchaseno)
            print(taxvalueone)
            if taxvalueone is None:
                taxvalueone = 0
            if taxvaluetwo is None:
                taxvaluetwo = 0
            if taxvaluethree is None:
                taxvaluethree = 0
            taxval = taxvalueone+taxvaluetwo+taxvaluethree
            print(taxval)
            txnamount1 = total_amount/100*taxvalueone
            txnamount2 = total_amount/100*taxvaluetwo
            txnamount3 = total_amount/100*taxvaluethree
            print(txnamount1)
            print(txnamount2)
            print(txnamount3)
            totalinvalue = total_amount+txnamount1+txnamount2+txnamount3
            print(totalinvalue)


            new_transaction = Transaction(Purchase_No=purchasenum,Invoice_No=form.invoiceno.data,Total_Value=form.totalvalue.data,Date = datetime.now(),Purchase_Date= form.purdate.data,Branch_code=branchcode,Vendor_code= vendorcode,
                                          Purchase_Details= billdescription,Item_details=itemdescription,Invoice_code= invoicecode,To_Usercode=tousercode, Txn_code1=taxcodeone, Txn_code2=taxcodetwo, Txn_code3=taxcodethree,User_code=usercode,
                                          Txn_value1= txnamount1,Txn_value2=txnamount2,Txn_value3=txnamount3,Total_Invalue=totalinvalue,Attachment_docs=image_url,Pay_Type=payment,initiate_User_Code=usercode)
            new_flow = FlowControlMaster(Purchase_No=purchasenum,Create_Date=datetime.now(),Access_Date=datetime.now(), Vendor_Code=vendorcode,Total_Invalue=totalinvalue,From_User=usercode,From_Branch=fromuserbranch,To_User=tousercode,To_Branch=touserbranch,User_Level=fromuserlevel,Comments=comments,Flow_Flag="N")
            db.session.add(new_transaction)
            db.session.add(new_flow)
            db.session.commit()
            flash('Data added successfully')
    except exc.IntegrityError as e:
        db.session().rollback()
        flash('Invoice already exists')

    user = format(current_user.Username)
    invoices = InvoiceMaster.query.all()
    taxes = TaxMaster.query.all()
    users = UserMaster.query.all()
    branches = BranchMaster.query.all()
    vendors = VendorMaster.query.all()




    form.invoiceno.data = ""
    form.totalvalue.data = ""
    form.purdate.data = ""
    return render_template('transaction.html', form=form, user=user, invoices = invoices, taxes=taxes, users=users, branches=branches,vendors = vendors,purchasenum=purchasenum,user_levels=user_levels)


@app.route('/view', methods=['GET', 'POST'])
def flow_control():
    form = Transactionform()
    transaction = Transaction.query.all()
    users = UserMaster.query.all()
    branch = BranchMaster.query.all()
    vendor = VendorMaster.query.all()
    invoices = InvoiceMaster.query.all()
    level = UserMaster.query.all()

    user = format(current_user.Username)
    print(user)
    current_user_code = format(current_user.user_code)

    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.To_User == current_user_code,FlowControlMaster.Flow_Flag != "Y").all()
    print(current_user_code)
    reject_counts = db.session.query(func.count(FlowControlMaster.Flag_Reject)).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
        FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Flow_Flag)).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
        FlowControlMaster.Flow_Flag == "N").scalar()
    #print(details)

    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()

    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()

    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    n_level = int(next_level_add)
    #print(next_level_convert_int_to_string)

    user_levels = db.session.query(UserMaster.Username,UserMaster.user_code).filter_by(user_level=next_level_convert_int_to_string).all()
    #print(type(user_levels))

    # details = db.session.query(Transaction, BranchMaster,  VendorMaster, InvoiceMaster,UserMaster).join(BranchMaster,BranchMaster.code == Transaction.Branch_code).join(VendorMaster,VendorMaster.vendor_code == Transaction.Vendor_code).join(InvoiceMaster,InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).all()
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    print(from_user)

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
        if request.method == "POST":
            purchase = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Auth_flag: "A"})
            flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update(
                {FlowControlMaster.Flow_Flag: "Y"})
            flow = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date,
                                         Access_Date=datetime.now(), Vendor_Code=vendor_name, Total_Invalue=totalvalue,
                                         From_User=current_user_code, From_Branch=user_code, To_User=current_user_code,
                                       To_Branch=to_user_branchcode, User_Level=from_user, Comments=user_comments, Flow_Flag = "Y")
            db.session.add(flow)
            db.session.commit()
            details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                       UserMaster).join(Transaction,
                                                        Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                 VendorMaster.vendor_code == Transaction.Vendor_code).join(
                InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                           UserMaster.user_code == Transaction.User_code).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y").all()

        return render_template('userlast.html', user=user, transaction=transaction, branch=branch, vendor=vendor,
                               details=details, user_levels=user_levels, form=form)



    if request.method == "POST":


        flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno,To_User=current_user_code).update({FlowControlMaster.Flow_Flag: "Y"})
        flow_data = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date, Access_Date=datetime.now(),
                                      Vendor_Code=vendor_name, Total_Invalue=totalvalue, From_User=current_user_code,
                                      From_Branch=user_code, To_User=to_user_code, To_Branch=to_user_branchcode,
                                      User_Level=from_user, Comments=user_comments,Flow_Flag="N")
        print(flow_data)
        db.session.add(flow_data)
        db.session.commit()
        details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                   UserMaster).join(Transaction,
                                                    Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
            BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                             VendorMaster.vendor_code == Transaction.Vendor_code).join(
            InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                       UserMaster.user_code == Transaction.User_code).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y").all()

    return render_template('vendorwiseinvoice.html', user=user, transaction=transaction, branch=branch, vendor=vendor,
                           details=details, user_levels=user_levels, form=form)


#### TRANSACT ONLY ####
@app.route('/transactlevel',methods=['GET', 'POST'])
@login_required
def viewtransactionlevel():
    form = Transactionform()
    user = format(current_user.Username)
    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()
    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                               UserMaster).join(Transaction,
                                                Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
        BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                         VendorMaster.vendor_code == Transaction.Vendor_code).join(
        InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                   UserMaster.user_code == Transaction.User_code).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",
        FlowControlMaster.Flag_Reject == None).all()
    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()

    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
        FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
        FlowControlMaster.Flow_Flag == "N").scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).scalar()

    ####DATE RANGE####
    if request.method == "POST":
        if request.form.get('filter') != None:
            from_date = request.form.get('fromdate')
            to_date = request.form.get('todate')
            print('from_date', from_date)
            print('to_date', to_date)
            details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                       UserMaster).join(Transaction,
                                                        Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                 VendorMaster.vendor_code == Transaction.Vendor_code).join(
                InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                           UserMaster.user_code == Transaction.User_code).filter(
                func.DATE(Transaction.Date).between(from_date, to_date), FlowControlMaster.To_User == current_user_code,
                                                                         FlowControlMaster.Flow_Flag != "Y",
                                                                         FlowControlMaster.Flag_Reject == None).all()
            print(type(from_date))
            print(type(to_date))

            if from_date == '' and to_date == '':
                details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                           UserMaster).join(Transaction,
                                                            Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                    BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                     VendorMaster.vendor_code == Transaction.Vendor_code).join(
                    InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                               UserMaster.user_code == Transaction.User_code).filter(
                    FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",
                    FlowControlMaster.Flag_Reject == None).all()


    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    print(next_level)
    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    print(next_level_convert_int_to_string)

    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_convert_int_to_string).all()
    print(user_levels)
    taxone = request.form.get('taxo', None)
    print(taxone)
    taxtwo = request.form.get('taxtw', None)
    taxthree = request.form.get('taxth', None)
    vendorname = request.form.get('vendorname', None)
    invoicename = request.form.get('invoicename', None)
    branchname = request.form.get('branchname', None)
    purchasedate = request.form.get('purchasedate', None)
    billdescription = request.form.get('bill', None)
    itemdescription = request.form.get('item', None)
    assignuser = request.form.get('assignto', None)
    comments = request.form.get('comment', None)
    payment = request.form.get('paytype', None)
    total_amount = form.totalvalue.data
    tds_percent = request.form.get('tds',None)
    print(type(tds_percent))
    print(assignuser)
    print(purchasedate)
    user = format(current_user.Username)
    purchasenum = db.session.query(PurchaseNumber.Purchase_No).scalar()
    print(purchasenum)
    purchase = PurchaseNumber.query.filter_by(Purchase_No=purchasenum).update(
        {PurchaseNumber.Purchase_No: purchasenum + 1})
    db.session.commit()


    #tax_val2 = [value for value in taxvaluetwo]
    #tax_val3 = [value for value in taxvaluethree]
    #amount = total_amount




    try:
        form = Transactionform()
        if form.validate_on_submit():
            total_amount = form.totalvalue.data
            usercode = db.session.query(UserMaster.user_code).filter_by(user_code=current_user_code).first()
            fromuserbranch = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).first()
            taxcodeone = db.session.query(TaxMaster.taxcode).filter_by(taxname=taxone).first()
            taxcodetwo = db.session.query(TaxMaster.taxcode).filter_by(taxname=taxtwo).first()
            taxcodethree = db.session.query(TaxMaster.taxcode).filter_by(taxname=taxthree).first()
            taxvalueone = db.session.query(TaxMaster.taxpercent).filter_by(taxname=taxone).scalar()
            taxvaluetwo = db.session.query(TaxMaster.taxpercent).filter_by(taxname=taxtwo).scalar()
            taxvaluethree = db.session.query(TaxMaster.taxpercent).filter_by(taxname=taxthree).scalar()
            branchcode = db.session.query(BranchMaster.code).filter_by(place=branchname).first()
            invoicecode = db.session.query(InvoiceMaster.invoicecode).filter_by(invoicename=invoicename).first()
            vendorcode = db.session.query(VendorMaster.vendor_code).filter_by(vendor_name=vendorname).first()
            tousercode = db.session.query(UserMaster.user_code).filter_by(Username=assignuser).first()
            touserbranch = db.session.query(UserMaster.branchcode).filter_by(Username=assignuser).first()
            touserlevel = db.session.query(UserMaster.user_level).filter_by(Username=assignuser).first()
            fromuserlevel = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).first()
            image_filename = photos.save(form.image.data)
            image_url = photos.url(image_filename)
            purchaseno = db.session.query(PurchaseNumber.Purchase_No).scalar()
            print(purchaseno)
            print(taxvalueone)
            if taxvalueone is None:
                taxvalueone = 0
            if taxvaluetwo is None:
                taxvaluetwo = 0
            if taxvaluethree is None:
                taxvaluethree = 0
            taxval = taxvalueone+taxvaluetwo+taxvaluethree
            print(taxval)
            tds_amount_value = int(tds_percent)/100*total_amount
            tds_total_value = total_amount - tds_amount_value
            txnamount1 = tds_total_value / 100 * taxvalueone
            txnamount2 = tds_total_value / 100 * taxvaluetwo
            txnamount3 = tds_total_value / 100 * taxvaluethree
            print(txnamount1)
            print(txnamount2)
            print(txnamount3)
            totalinvalue = tds_total_value+txnamount1+txnamount2+txnamount3
            print(totalinvalue)


            new_transaction = Transaction(Purchase_No=purchasenum,Invoice_No=form.invoiceno.data,Total_Value=tds_total_value,Date = datetime.now(),Purchase_Date= form.purdate.data,Branch_code=branchcode,Vendor_code= vendorcode,
                                          Purchase_Details= billdescription,Item_details=itemdescription,Invoice_code= invoicecode,To_Usercode=tousercode, Txn_code1=taxcodeone, Txn_code2=taxcodetwo, Txn_code3=taxcodethree,User_code=usercode,
                                          Txn_value1= txnamount1,Txn_value2=txnamount2,Txn_value3=txnamount3,Total_Invalue=totalinvalue,Attachment_docs=image_url,Payment_Type=payment,initiate_User_Code=usercode,Total_Before_Value=form.totalvalue.data,Tds_Percentage=tds_percent,Tds_Amount=tds_amount_value)
            new_flow = FlowControlMaster(Purchase_No=purchasenum,Create_Date=datetime.now(),Access_Date=datetime.now(), Vendor_Code=vendorcode,Total_Invalue=totalinvalue,From_User=usercode,From_Branch=fromuserbranch,To_User=tousercode,To_Branch=touserbranch,User_Level=fromuserlevel,Comments=comments,Flow_Flag="N")
            db.session.add(new_transaction)
            db.session.add(new_flow)
            if request.form.get('check') == "Q":
                quickflag = Transaction.query.filter_by(Purchase_No=purchasenum).update({Transaction.Quick_Flag: "Q"})
            db.session.commit()
            details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                       UserMaster).join(Transaction,
                                                        Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                 VendorMaster.vendor_code == Transaction.Vendor_code).join(
                InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                           UserMaster.user_code == Transaction.User_code).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",
                FlowControlMaster.Flag_Reject == None).all()
            datas = db.session.query(Transaction, FlowControlMaster.Comments, FlowControlMaster.From_User, BranchMaster,
                                     VendorMaster, InvoiceMaster, UserMaster).join(FlowControlMaster,
                                                                                   FlowControlMaster.Purchase_No == Transaction.Purchase_No).join(
                BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                 VendorMaster.vendor_code == Transaction.Vendor_code).join(
                InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                           UserMaster.user_code == Transaction.User_code).filter(
                FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()

            reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
                FlowControlMaster.Flow_Flag != "Y").scalar()
            inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
                FlowControlMaster.Flow_Flag == "N").scalar()
            sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
                FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
            quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(
                Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()

            print(sent_counts)
            flash('Data added successfully')
    except exc.IntegrityError as e:
        db.session().rollback()
        flash('Invoice already exists')

    user = format(current_user.Username)
    invoices = InvoiceMaster.query.all()
    taxes = TaxMaster.query.all()
    users = UserMaster.query.all()
    branches = BranchMaster.query.all()
    vendors = VendorMaster.query.all()




    form.invoiceno.data = ""
    form.totalvalue.data = ""
    form.purdate.data = ""
    return render_template('transactonly.html', form=form, user=user, invoices = invoices, taxes=taxes, users=users, branches=branches,vendors = vendors,purchasenum=purchasenum,user_levels=user_levels,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts)

### VIEW ONLY ###
@app.route('/viewonly', methods=['GET', 'POST'])
def flow_controlonly():
    form = Transactionform()
    transaction = Transaction.query.all()
    users = UserMaster.query.all()
    branch = BranchMaster.query.all()
    vendor = VendorMaster.query.all()
    invoices = InvoiceMaster.query.all()
    level = UserMaster.query.all()

    user = format(current_user.Username)
    print(user)
    current_user_code = format(current_user.user_code)

    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.To_User == current_user_code,FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == None).all()
    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User,BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    reject_counts = db.session.query(func.count(FlowControlMaster.Flag_Reject)).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
        FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Flow_Flag)).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
        FlowControlMaster.Flow_Flag == "N").scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).scalar()

    print(current_user_code)
    #print(details)

    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()

    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()

    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    #print(next_level_convert_int_to_string)

    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_convert_int_to_string).all()
    #print(type(user_levels))

    # details = db.session.query(Transaction, BranchMaster,  VendorMaster, InvoiceMaster,UserMaster).join(BranchMaster,BranchMaster.code == Transaction.Branch_code).join(VendorMaster,VendorMaster.vendor_code == Transaction.Vendor_code).join(InvoiceMaster,InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).all()
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    print(from_user)

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
            purchase = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Auth_flag: "A"})
            flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update(
                {FlowControlMaster.Flow_Flag: "Y"})
            flow = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date,
                                     Access_Date=datetime.now(), Vendor_Code=vendor_name, Total_Invalue=totalvalue,
                                     From_User=current_user_code, From_Branch=user_code, To_User=current_user_code,
                                     To_Branch=user_code, User_Level=from_user, Comments=user_comments, Flow_Flag = "Y")
            updatetransactfromuser=Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
            updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: current_user_code})
            db.session.add(flow)
            db.session.commit()
            details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                       UserMaster).join(Transaction,
                                                        Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                 VendorMaster.vendor_code == Transaction.Vendor_code).join(
                InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                           UserMaster.user_code == Transaction.User_code).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == None).all()
            reject_counts = db.session.query(func.count(FlowControlMaster.Flag_Reject)).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
                FlowControlMaster.Flow_Flag != "Y").scalar()
            inbox_counts = db.session.query(func.count(FlowControlMaster.Flow_Flag)).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
                FlowControlMaster.Flow_Flag == "N").scalar()
            sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
                FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
            quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(
                Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()

            return render_template('userlast.html', user=user, transaction=transaction, branch=branch, vendor=vendor,
                               details=details, user_levels=user_levels, form=form,datas=datas,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts)


    if request.method == "POST" and request.form.get('action'):
        flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno,To_User=current_user_code).update({FlowControlMaster.Flow_Flag: "Y"})
        flow_data = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date, Access_Date=datetime.now(),
                                  Vendor_Code=vendor_name, Total_Invalue=totalvalue, From_User=current_user_code,
                                  From_Branch=user_code, To_User=to_user_code, To_Branch=to_user_branchcode,
                                  User_Level=from_user, Comments=user_comments,Flow_Flag="N")
        print(flow_data)
        updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
        updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: to_user_code})
        db.session.add(flow_data)
        db.session.commit()
        if current_user.user_level == 1:
            image_filename = photos.save(form.image.data)
            image_url = photos.url(image_filename)
            invoiceno = request.form.get('invoiceno', None)
            invoicename = request.form.get('invoicename', None)
            invoicecode = db.session.query(InvoiceMaster.invoicecode).filter_by(invoicename=invoicename).first()
            vendorname = request.form.get('vendorname', None)
            vendorcode = db.session.query(VendorMaster.vendor_code).filter_by(vendor_name=vendorname).first()
            total_amount = request.form.get('amount', None)
            print(type(total_amount))
            amount = float(total_amount)
            payment = request.form.get('paytype', None)
            tds_percent = request.form.get('tds', None)
            print(type(tds_percent))
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
            tds = float(tds_percent)
            print(tds)
            tds_amount_value = tds / 100 * amount
            tds_total_value = amount - tds_amount_value
            txnamount1 = tds_total_value / 100 * taxvalueone
            txnamount2 = tds_total_value / 100 * taxvaluetwo
            txnamount3 = tds_total_value / 100 * taxvaluethree
            totalinvalue = tds_total_value + txnamount1 + txnamount2 + txnamount3

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
            updatetds = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Tds_Percentage: tds_percent})
            updatebill = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Purchase_Details: billdescription})
            updateitem = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Item_details: itemdescription})
            updatetcode1 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_code1: taxcodeone})
            updatetcode2 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_code2: taxcodetwo})
            updatetcode3 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_code3: taxcodethree})
            updatetvalue1 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_value1: txnamount1})
            updatetvalue2 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_value2: txnamount2})
            updatetvalue3 = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Txn_value3: txnamount3})
            totalinvalue = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Total_Invalue: totalinvalue})
            totalval = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.Total_Value: tds_total_value})
            db.session.commit()
        details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                   UserMaster).join(Transaction,
                                                    Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
            BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                             VendorMaster.vendor_code == Transaction.Vendor_code).join(
            InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                       UserMaster.user_code == Transaction.User_code).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",
            FlowControlMaster.Flag_Reject == None).all()
        reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
            FlowControlMaster.Flow_Flag != "Y").scalar()
        inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
            FlowControlMaster.Flow_Flag == "N").scalar()
        sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
            FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
        quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(
            Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()
        details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                               UserMaster).join(Transaction,
                                                Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
        BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                         VendorMaster.vendor_code == Transaction.Vendor_code).join(
        InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                   UserMaster.user_code == Transaction.User_code).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == None).all()
        reject_counts = db.session.query(func.count(FlowControlMaster.Flag_Reject)).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
            FlowControlMaster.Flow_Flag != "Y").scalar()
        inbox_counts = db.session.query(func.count(FlowControlMaster.Flow_Flag)).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
            FlowControlMaster.Flow_Flag == "N").scalar()
        sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
            FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
        quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(
            Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()

        return render_template('viewonly.html', user=user, transaction=transaction, branch=branch, vendor=vendor,
                           details=details, user_levels=user_levels, form=form,datas=datas,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts)

    form = Transactionform()
    transaction = Transaction.query.all()
    users = UserMaster.query.all()
    branch = BranchMaster.query.all()
    vendor = VendorMaster.query.all()
    invoices = InvoiceMaster.query.all()
    level = UserMaster.query.all()

    user = format(current_user.Username)
    print(user)
    current_user_code = format(current_user.user_code)

    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                               UserMaster).join(Transaction,
                                                Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
        BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                         VendorMaster.vendor_code == Transaction.Vendor_code).join(
        InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                   UserMaster.user_code == Transaction.User_code).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == None).all()
    reject_counts = db.session.query(func.count(FlowControlMaster.Flag_Reject)).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
        FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Flow_Flag)).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
        FlowControlMaster.Flow_Flag == "N").scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).scalar()

    print(current_user_code)
    # print(details)

    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()

    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()

    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    # print(next_level_convert_int_to_string)

    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_convert_int_to_string).all()
    # print(type(user_levels))

    #details = db.session.query(Transaction, BranchMaster,  VendorMaster, InvoiceMaster,UserMaster).join(BranchMaster,BranchMaster.code == Transaction.Branch_code).join(VendorMaster,VendorMaster.vendor_code == Transaction.Vendor_code).join(InvoiceMaster,InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).all()
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    print(from_user)

    user_code = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    user_branch = db.session.query(BranchMaster.place).filter_by(code=user_code).scalar()

    ven_code = request.form.get('vendorname')
    vendor_name = db.session.query(VendorMaster.vendor_code).filter_by(vendor_name=ven_code).scalar()

    purno = request.form.get('purno')
    print('purcahse no',purno)
    purchase_date = request.form.get('purchasedate')
    totalvalue = request.form.get('amount')
    to_user = request.form.get('user')
    user_comments = request.form.get('body')

    from_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    to_user_code = db.session.query(UserMaster.user_code).filter_by(Username=to_user).scalar()
    return_user_code = db.session.query(FlowControlMaster.From_User.distinct()).filter_by(Purchase_No=purno,
                                                                            To_User=current_user_code,Flag_Reject=None).scalar()

    return_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(user_code=return_user_code).scalar()
    print('purcahse no', purno)
    print('form user branch code ', from_user_branchcode)
    print('return user code ', return_user_code)
    print('return user branch code',return_user_branchcode)
    if not user_levels:
        if request.method == "POST" and request.form.get('act'):

            purchase = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Auth_flag: "R"})
            flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update(
                {FlowControlMaster.Flow_Flag: "Y"})
            flow = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date,
                                     Access_Date=datetime.now(), Vendor_Code=vendor_name, Total_Invalue=totalvalue,
                                     From_User=current_user_code, From_Branch=from_user_branchcode,To_User=return_user_code,To_Branch=return_user_branchcode,
                                     User_Level=from_user, Comments=user_comments,
                                     Flow_Flag="N",Flag_Reject="R")
            #flagreject = FlowControlMaster.query.filter_by(Purchase_No=purno, From_User=current_user_code, To_User=return_user_code).update({FlowControlMaster.Flag_Reject: "R"})
            updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
            updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: return_user_code})
            db.session.add(flow)
            db.session.commit()
            details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                       UserMaster).join(Transaction,
                                                        Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                 VendorMaster.vendor_code == Transaction.Vendor_code).join(
                InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                           UserMaster.user_code == Transaction.User_code).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == None).all()
            reject_counts = db.session.query(func.count(FlowControlMaster.Flag_Reject)).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
                FlowControlMaster.Flow_Flag != "Y").scalar()
            inbox_counts = db.session.query(func.count(FlowControlMaster.Flow_Flag)).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
                FlowControlMaster.Flow_Flag == "N").scalar()
            sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
                FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
            quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(
                Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()

        return render_template('userlast.html', user=user, transaction=transaction, branch=branch, vendor=vendor,
                               details=details, user_levels=user_levels, form=form, datas=datas,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts)

    if request.method == "POST" and request.form.get('act'):
        flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update({FlowControlMaster.Flow_Flag: "Y"})
        flow_data = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date, Access_Date=datetime.now(),
                                      Vendor_Code=vendor_name, Total_Invalue=totalvalue, From_User=current_user_code,
                                      From_Branch=from_user_branchcode,To_User=return_user_code,To_Branch=return_user_branchcode,
                                      User_Level=from_user, Comments=user_comments, Flow_Flag="N",Flag_Reject="R")
        updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
        updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: return_user_code})
        #flagreject = FlowControlMaster.query.filter_by(Purchase_No=purno, From_User=current_user_code,To_User=return_user_code).update({FlowControlMaster.Flag_Reject: "R"})
        print(flow_data)
        print("reject called")
        db.session.add(flow_data)
        db.session.commit()
        details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster, UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == None).all()
        reject_counts = db.session.query(func.count(FlowControlMaster.Flag_Reject)).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
            FlowControlMaster.Flow_Flag != "Y").scalar()
        inbox_counts = db.session.query(func.count(FlowControlMaster.Flow_Flag)).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
            FlowControlMaster.Flow_Flag == "N").scalar()
        sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
            FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
        quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(
            Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()

    return render_template('viewonly.html', user=user, transaction=transaction, branch=branch, vendor=vendor,
                       details=details, user_levels=user_levels, form=form,datas=datas,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts)



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
    print(user)
    current_user_code = format(current_user.user_code)
    ####DATE RANGE####
    if request.method == "POST":
        if request.form.get('filter') != None:
            from_date = request.form.get('fromdate')
            to_date = request.form.get('todate')
            print('from_date', from_date)
            print('to_date', to_date)
            details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                       UserMaster).join(Transaction,
                                                        Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                 VendorMaster.vendor_code == Transaction.Vendor_code).join(
                InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                           UserMaster.user_code == Transaction.User_code).filter(
                func.DATE(Transaction.Date).between(from_date, to_date), FlowControlMaster.To_User == current_user_code,
                                                                         FlowControlMaster.Flow_Flag != "Y",
                                                                         FlowControlMaster.Flag_Reject == None).all()
            print(type(from_date))
            print(type(to_date))

            if from_date == '' and to_date == '':
                details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                           UserMaster).join(Transaction,
                                                            Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                    BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                     VendorMaster.vendor_code == Transaction.Vendor_code).join(
                    InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                               UserMaster.user_code == Transaction.User_code).filter(
                    FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",
                    FlowControlMaster.Flag_Reject == None).all()

    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.To_User == current_user_code,FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == "R").all()
    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
        FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
        FlowControlMaster.Flow_Flag == "N").scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).scalar()

    print(current_user_code)
    #print(details)

    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()

    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()

    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    #print(next_level_convert_int_to_string)

    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_convert_int_to_string).all()
    #print(type(user_levels))

    # details = db.session.query(Transaction, BranchMaster,  VendorMaster, InvoiceMaster,UserMaster).join(BranchMaster,BranchMaster.code == Transaction.Branch_code).join(VendorMaster,VendorMaster.vendor_code == Transaction.Vendor_code).join(InvoiceMaster,InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).all()
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    print(from_user)

    user_code = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    user_branch = db.session.query(BranchMaster.place).filter_by(code=user_code).scalar()

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
            purchase = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Auth_flag: "A"})
            flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update(
                {FlowControlMaster.Flow_Flag: "Y"})
            flow = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date,
                                     Access_Date=datetime.now(), Vendor_Code=vendor_name, Total_Invalue=totalvalue,
                                     From_User=current_user_code, From_Branch=user_code, To_User=current_user_code,
                                     To_Branch=to_user_branchcode, User_Level=from_user, Comments=user_comments, Flow_Flag = "Y")
            updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
            updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.To_Usercode: current_user_code})
            db.session.add(flow)
            db.session.commit()
            details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                       UserMaster).join(Transaction,
                                                        Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                 VendorMaster.vendor_code == Transaction.Vendor_code).join(
                InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                           UserMaster.user_code == Transaction.User_code).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == "R").all()
            reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
                FlowControlMaster.Flow_Flag != "Y").scalar()
            inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
                FlowControlMaster.Flow_Flag == "N").scalar()
            sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
                FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
            quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(
                Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()

        return render_template('userlast.html', user=user, transaction=transaction, branch=branch, vendor=vendor,
                               details=details, user_levels=user_levels, form=form,datas=datas,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts)


    if request.method == "POST":
        flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno,To_User=current_user_code).update({FlowControlMaster.Flow_Flag: "Y"})
        flow_data = FlowControlMaster(Purchase_No=purno, Create_Date=purchase_date, Access_Date=datetime.now(),
                                  Vendor_Code=vendor_name, Total_Invalue=totalvalue, From_User=current_user_code,
                                  From_Branch=user_code, To_User=to_user_code, To_Branch=to_user_branchcode,
                                  User_Level=from_user, Comments=user_comments,Flow_Flag="N")
        print(flow_data)
        updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: current_user_code})
        updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update({Transaction.User_code: to_user_code})
        db.session.add(flow_data)
        db.session.commit()
        details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                               UserMaster).join(Transaction,
                                                Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
        BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                         VendorMaster.vendor_code == Transaction.Vendor_code).join(
        InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                   UserMaster.user_code == Transaction.User_code).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y", FlowControlMaster.Flag_Reject == "R").all()
        reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
            FlowControlMaster.Flow_Flag != "Y").scalar()
        inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
            FlowControlMaster.Flow_Flag == "N").scalar()
        sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
            FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
        quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(
            Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()

        return render_template('rejectonly.html', user=user, transaction=transaction, branch=branch, vendor=vendor,
                           details=details, user_levels=user_levels, form=form, datas=datas,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts)

    form = Transactionform()
    transaction = Transaction.query.all()
    users = UserMaster.query.all()
    branch = BranchMaster.query.all()
    vendors = VendorMaster.query.all()
    invoices = InvoiceMaster.query.all()
    level = UserMaster.query.all()

    user = format(current_user.Username)
    print(user)
    current_user_code = format(current_user.user_code)

    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                               UserMaster).join(Transaction,
                                                Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
        BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                         VendorMaster.vendor_code == Transaction.Vendor_code).join(
        InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                   UserMaster.user_code == Transaction.User_code).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",FlowControlMaster.Flag_Reject == "R").all()
    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
        FlowControlMaster.Flow_Flag != "Y").scalar()
    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
        FlowControlMaster.Flow_Flag == "N").scalar()
    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).scalar()

    print(current_user_code)
    # print(details)

    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()

    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()

    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    # print(next_level_convert_int_to_string)

    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_convert_int_to_string).all()
    # print(type(user_levels))

    #details = db.session.query(Transaction, BranchMaster,  VendorMaster, InvoiceMaster,UserMaster).join(BranchMaster,BranchMaster.code == Transaction.Branch_code).join(VendorMaster,VendorMaster.vendor_code == Transaction.Vendor_code).join(InvoiceMaster,InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).all()
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    print(from_user)

    user_code = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    user_branch = db.session.query(BranchMaster.place).filter_by(code=user_code).scalar()

    ven_code = request.form.get('vendorname')
    vendor_name = db.session.query(VendorMaster.vendor_code).filter_by(vendor_name=ven_code).scalar()

    purno = request.form.get('purno')
    purchase_date = request.form.get('purchasedate')
    totalvalue = request.form.get('amount')
    to_user = request.form.get('user')
    user_comments = request.form.get('body')

    from_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    to_user_code = db.session.query(UserMaster.user_code).filter_by(Username=to_user).scalar()
    return_user_code = db.session.query(FlowControlMaster.From_User.distinct()).filter_by(Purchase_No=purno,
                                                                            To_User=current_user_code,Flag_Reject=None).scalar()
    print(return_user_code)
    return_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(user_code=return_user_code).scalar()

    if not user_levels:
        if request.method == "POST" and request.form.get('act'):
            purchase = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.Auth_flag: "R"})
            flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update(
                {FlowControlMaster.Flow_Flag: "Y"})
            flow = FlowControlMaster(Purchase_No=purno, Create_Date=create_date,
                                     Access_Date=datetime.now(), Vendor_Code=vendor_name, Total_Invalue=totalvalue,
                                     From_User=current_user_code, From_Branch=from_user_branchcode,
                                     To_User=return_user_code, To_Branch=return_user_branchcode,
                                     User_Level=from_user, Comments=user_comments,
                                     Flow_Flag="N", Flag_Reject="R")
            # flagreject = FlowControlMaster.query.filter_by(Purchase_No=purno, From_User=current_user_code, To_User=return_user_code).update({FlowControlMaster.Flag_Reject: "R"})
            updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.User_code: current_user_code})
            updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update(
                {Transaction.To_Usercode: return_user_code})
            db.session.add(flow)
            db.session.commit()
            details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                       UserMaster).join(Transaction,
                                                        Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                 VendorMaster.vendor_code == Transaction.Vendor_code).join(
                InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                           UserMaster.user_code == Transaction.User_code).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",
                FlowControlMaster.Flag_Reject == None).all()
            reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
                FlowControlMaster.Flow_Flag != "Y").scalar()
            inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
                FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
                FlowControlMaster.Flow_Flag == "N").scalar()
            sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
                FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
            quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(
                Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()

        return render_template('userlast.html', user=user, transaction=transaction, branch=branch, vendor=vendor,
                               details=details, user_levels=user_levels, form=form, datas=datas,
                               reject_counts=reject_counts, inbox_counts=inbox_counts, sent_counts=sent_counts,
                               quick_counts=quick_counts)

    if request.method == "POST" and request.form.get('act'):
        flowflag = FlowControlMaster.query.filter_by(Purchase_No=purno, To_User=current_user_code).update(
            {FlowControlMaster.Flow_Flag: "Y"})
        flow_data = FlowControlMaster(Purchase_No=purno, Create_Date=create_date, Access_Date=datetime.now(),
                                      Vendor_Code=vendor_name, Total_Invalue=totalvalue, From_User=current_user_code,
                                      From_Branch=from_user_branchcode, To_User=return_user_code,
                                      To_Branch=return_user_branchcode,
                                      User_Level=from_user, Comments=user_comments, Flow_Flag="N", Flag_Reject="R")
        updatetransactfromuser = Transaction.query.filter_by(Purchase_No=purno).update(
            {Transaction.User_code: current_user_code})
        updatetransacttouser = Transaction.query.filter_by(Purchase_No=purno).update(
            {Transaction.To_Usercode: return_user_code})
        # flagreject = FlowControlMaster.query.filter_by(Purchase_No=purno, From_User=current_user_code,To_User=return_user_code).update({FlowControlMaster.Flag_Reject: "R"})
        print(flow_data)
        print("reject called")
        db.session.add(flow_data)
        db.session.commit()
        details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                   UserMaster).join(Transaction,
                                                    Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
            BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                             VendorMaster.vendor_code == Transaction.Vendor_code).join(
            InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                       UserMaster.user_code == Transaction.User_code).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",
            FlowControlMaster.Flag_Reject == None).all()
        reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
            FlowControlMaster.Flow_Flag != "Y").scalar()
        inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
            FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
            FlowControlMaster.Flow_Flag == "N").scalar()
        sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
            FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
        quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(
            Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()
    for data in datas:
        print(data[1])
    return render_template('rejectonly.html', user=user, transaction=transaction, branch=branch, vendor=vendor,invoices=invoices,vendors=vendors,
                           details=details, user_levels=user_levels, form=form, datas=datas,taxes=taxes,
                           reject_counts=reject_counts, inbox_counts=inbox_counts, sent_counts=sent_counts,
                           quick_counts=quick_counts)


@app.route('/sentonly', methods=['GET', 'POST'])
def sent_controlonly():
    form = Viewform()
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

    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.From_User == current_user_code).all()

    print(current_user_code)
    #print(details)

    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()

    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()

    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    #print(next_level_convert_int_to_string)

    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_add).all()
    print('user_levels is',user_level)

    # details = db.session.query(Transaction, BranchMaster,  VendorMaster, InvoiceMaster,UserMaster).join(BranchMaster,BranchMaster.code == Transaction.Branch_code).join(VendorMaster,VendorMaster.vendor_code == Transaction.Vendor_code).join(InvoiceMaster,InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).all()
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    print(from_user)

    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R",
        FlowControlMaster.Flow_Flag != "Y").scalar()

    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,
        FlowControlMaster.Flow_Flag == "N").scalar()

    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(
        FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
    print(sent_counts)
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(
        Transaction.Quick_Flag == "Q", Transaction.Auth_flag == None).scalar()


    print("inbox count is :", inbox_counts)
    print("Rejected count is :", reject_counts)

    user_code = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    user_branch = db.session.query(BranchMaster.place).filter_by(code=user_code).scalar()

    ven_code = request.form.get('vendorname')
    vendor_name = db.session.query(VendorMaster.vendor_code).filter_by(vendor_name=ven_code).scalar()

    purno = request.form.get('purno')
    yo_user = current_user_code

    print('purchase no is :', purno)
    print('To user is :', yo_user)

    purchase_date = request.form.get('purchasedate')
    totalvalue = request.form.get('amount')
    to_user = request.form.get('user')
    user_comments = request.form.get('body')

    to_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(Username=to_user).scalar()
    to_user_code = db.session.query(UserMaster.user_code).filter_by(Username=to_user).scalar()
    to_userbranch = db.session.query(BranchMaster.place).filter_by(code=to_user_branchcode).scalar()



    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    for data in datas:
        print(data[0].Purchase_No)
        print(data[1])
        print(data[2])

    if request.method == "POST":
        if request.form.get('filter') != None:
            from_date = request.form.get('fromdate')
            to_date = request.form.get('todate')
            print('from_date', from_date)
            print('to_date', to_date)
            details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                       UserMaster).join(Transaction,
                                                        Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                 VendorMaster.vendor_code == Transaction.Vendor_code).join(
                InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                           UserMaster.user_code == Transaction.User_code).filter(
                func.DATE(Transaction.Date).between(from_date, to_date), FlowControlMaster.To_User == current_user_code,
                                                                         FlowControlMaster.Flow_Flag != "Y",
                                                                         FlowControlMaster.Flag_Reject == None).all()
            for det in details:
                print(det[1].Purchase_No)
            print(type(from_date))
            print(type(to_date))

            if from_date == '' and to_date == '':
                details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                           UserMaster).join(Transaction,
                                                            Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                    BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                     VendorMaster.vendor_code == Transaction.Vendor_code).join(
                    InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                               UserMaster.user_code == Transaction.User_code).filter(
                    FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",
                    FlowControlMaster.Flag_Reject == None).all()

    ######### user level is 6 ##############

    return render_template('sentonly.html', user=user, transaction=transaction, branch=branch, vendor=vendor,details=details, user_levels=user_levels, form=form,datas=datas,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts,transact=transact)

@app.route('/quickonly', methods=['GET', 'POST'])
def quick_controlonly():
    form = Transactionform()
    transaction = Transaction.query.all()
    users = UserMaster.query.all()
    branch = BranchMaster.query.all()
    vendor = VendorMaster.query.all()
    invoices = InvoiceMaster.query.all()
    level = UserMaster.query.all()

    user = format(current_user.Username)
    print(user)
    current_user_code = format(current_user.user_code)

    details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(Transaction,Transaction.Purchase_No == FlowControlMaster.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).all()

    print(current_user_code)
    #print(details)

    current_user_code = format(current_user.user_code)
    user_level = UserMaster.query.all()

    next_level = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()

    next_level_convert_string_to_int = int(next_level)
    next_level_add = next_level_convert_string_to_int + 1
    next_level_convert_int_to_string = str(next_level_add)
    #print(next_level_convert_int_to_string)

    user_levels = db.session.query(UserMaster.Username).filter_by(user_level=next_level_add).all()
    print('user_levels is',user_level)

    ####DATE RANGE####
    if request.method == "POST":
        if request.form.get('filter') != None:
            from_date = request.form.get('fromdate')
            to_date = request.form.get('todate')
            print('from_date', from_date)
            print('to_date', to_date)
            details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                       UserMaster).join(Transaction,
                                                        Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                 VendorMaster.vendor_code == Transaction.Vendor_code).join(
                InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                           UserMaster.user_code == Transaction.User_code).filter(
                func.DATE(Transaction.Date).between(from_date, to_date), FlowControlMaster.To_User == current_user_code,
                                                                         FlowControlMaster.Flow_Flag != "Y",
                                                                         FlowControlMaster.Flag_Reject == None).all()
            print(type(from_date))
            print(type(to_date))

            if from_date == '' and to_date == '':
                details = db.session.query(FlowControlMaster, Transaction, BranchMaster, VendorMaster, InvoiceMaster,
                                           UserMaster).join(Transaction,
                                                            Transaction.Purchase_No == FlowControlMaster.Purchase_No).join(
                    BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster,
                                                                                     VendorMaster.vendor_code == Transaction.Vendor_code).join(
                    InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,
                                                                                               UserMaster.user_code == Transaction.User_code).filter(
                    FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flow_Flag != "Y",
                    FlowControlMaster.Flag_Reject == None).all()

    # details = db.session.query(Transaction, BranchMaster,  VendorMaster, InvoiceMaster,UserMaster).join(BranchMaster,BranchMaster.code == Transaction.Branch_code).join(VendorMaster,VendorMaster.vendor_code == Transaction.Vendor_code).join(InvoiceMaster,InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).all()
    from_user = db.session.query(UserMaster.user_level).filter_by(user_code=current_user_code).scalar()
    print(from_user)

    reject_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == "R", FlowControlMaster.Flow_Flag != "Y").scalar()

    inbox_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.To_User == current_user_code, FlowControlMaster.Flag_Reject == None,FlowControlMaster.Flow_Flag == "N").scalar()

    sent_counts = db.session.query(func.count(FlowControlMaster.Purchase_No.distinct())).filter(FlowControlMaster.From_User == current_user_code, FlowControlMaster.Flag_Reject == None).scalar()
    print(sent_counts)
    quick_counts = db.session.query(func.count(Transaction.Purchase_No.distinct())).filter(Transaction.Quick_Flag == "Q",Transaction.Auth_flag == None).scalar()

    print("inbox count is :", inbox_counts)
    print("Rejected count is :", reject_counts)

    user_code = db.session.query(UserMaster.branchcode).filter_by(user_code=current_user_code).scalar()
    user_branch = db.session.query(BranchMaster.place).filter_by(code=user_code).scalar()

    ven_code = request.form.get('vendorname')
    vendor_name = db.session.query(VendorMaster.vendor_code).filter_by(vendor_name=ven_code).scalar()

    purno = request.form.get('purno')
    yo_user = current_user_code

    print('purchase no is :', purno)
    print('To user is :', yo_user)

    purchase_date = request.form.get('purchasedate')
    totalvalue = request.form.get('amount')
    to_user = request.form.get('user')
    user_comments = request.form.get('body')

    to_user_branchcode = db.session.query(UserMaster.branchcode).filter_by(Username=to_user).scalar()
    to_user_code = db.session.query(UserMaster.user_code).filter_by(Username=to_user).scalar()
    to_userbranch = db.session.query(BranchMaster.place).filter_by(code=to_user_branchcode).scalar()



    datas = db.session.query(Transaction, FlowControlMaster.Comments,FlowControlMaster.From_User, BranchMaster, VendorMaster, InvoiceMaster,UserMaster).join(FlowControlMaster,FlowControlMaster.Purchase_No == Transaction.Purchase_No).join( BranchMaster, BranchMaster.code == Transaction.Branch_code).join(VendorMaster, VendorMaster.vendor_code == Transaction.Vendor_code).join( InvoiceMaster, InvoiceMaster.invoicecode == Transaction.Invoice_code).join(UserMaster,UserMaster.user_code == Transaction.User_code).filter(FlowControlMaster.Purchase_No == Transaction.Purchase_No).all()
    for data in datas:
        print(data[0].Purchase_No)
        print(data[1])
        print(data[2])

    ######### user level is 6 ##############

    return render_template('quickonly.html', user=user, transaction=transaction, branch=branch, vendor=vendor,details=details, user_levels=user_levels, form=form,datas=datas,reject_counts=reject_counts,inbox_counts=inbox_counts,sent_counts=sent_counts,quick_counts=quick_counts)


if __name__ == '__main__':
    app.run(debug=True,host='192.168.0.55',port=5000)
