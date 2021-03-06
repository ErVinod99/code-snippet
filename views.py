from flask import Flask, render_template, request, flash, session, redirect, url_for
from app import app

from app import mail, Message
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
import json
from models import *
from app import URLSafeTimedSerializer, SignatureExpired, t

from app import login_manager, login_required, logout_user, current_user, login_user
from flask_mysqldb import MySQLdb
import random
import string
import pdb


#from models import Studentdtls

#from forms import Studentdtls





@app.route('/')
def index():

    return render_template('index.html')



 

@app.route('/student_login', methods = ['GET','POST'])
def student_login():

    if request.method == "POST":
        student_id = request.form['student_id']
        student_password = request.form['student_password']


        user = Students_data.query.filter_by(student_id=student_id).first()
        subject = user.subjects
        splitted_subjects = subject.split(",")
        sub = len(splitted_subjects)

        
        
        print(sub)

        if user and bcrypt.check_password_hash(user.student_password, student_password):
            
            if user.payment_status is True:
                login_user(user)
                payment_status = user.payment_status
                msg = flash('You are now logged in..','success')
                return redirect(url_for('student_dashboard', msg=msg, user=user, sub= sub))
            elif sub == 2:
                    login_user(user)
                    msg = flash('Your payment is pending, please pay for accessing videos','danger')
                    return redirect(url_for('thankyou2', msg=msg, user = user))
            else:
                login_user(user)
                msg = flash('Your payment is pending, please pay for accessing videos','danger')
                return redirect(url_for('thankyou1', msg=msg, user=user))

        else:
            flash('Login Unsuccessful. Please check Student_id and password', 'danger')

            
    return render_template('student_login.html')   






@app.route('/student_registration', methods=['GET', 'POST'])
def student_registration():

    if request.method == "POST":

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        student_id =  random.randrange(100000,999999)
        student_email = request.form['student_email']
        parent_email = request.form['parent_email']
        student_phone_number = request.form['student_phone_number']
        parent_phone_number = request.form['parent_phone_number']
        city = request.form['city']
        standard = request.form['standard']
        current_address = request.form['current_address']
        board = request.form['board']

        subj = request.form.getlist('sub')
        #print(subj)

        subjects = ','.join(subj)


        auto_password = random.randrange(100000,999999)

        string_pass = str(auto_password)

        hashed_password = bcrypt.generate_password_hash(string_pass).decode('utf-8')

        student_password = hashed_password

        user = Students_data(student_id, first_name, last_name, student_email, parent_email , student_phone_number, parent_phone_number, city, standard, current_address, board, subjects, student_password)
        db.session.add(user)
        db.session.commit()

        ### Confirmation mail code  ###
        '''
        token = t.dumps(student_email, salt='email-confirm')
        msg = Message('Confirmation email', sender='enquiry@maiiceducation.com', recipients=[student_email])
        link = url_for('confirm_email', token=token, _external=True )
        msg.body = 'Your link is {}'.format(link)
        mail.send(msg)
        '''


        msg = Message(subject='Login details...', recipients = [student_email, parent_email])
        msg.body = "Hello {} {}, Your login details are >> Student ID = {}, Password = {}".format(first_name, last_name, student_id, auto_password)
        mail.send(msg)


        msg = flash('Registration successful ! Login details are on your mail.', 'success')
        return render_template('student_login.html', msg = msg, subj= subj)

    return render_template('student_registration.html')      




        #app.config['MAIL_USERNAME']= student_email
        #msg = Message(subject='Login details...', recipients = [app.config['MAIL_USERNAME']])
        #msg.body = "Hello {}, you have successfully registered to MAIIC Technology for {} subject !! your login details will provide after successful payment, thank you ! student ID = {} , student Password = {}  ".format(first_name, subjects, student_id, student_password)
        #msg.body = ""
        #mail.send(msg)





'''
@app.route('/send_sms')
def send_sms():


    first_name = sms_data[0]
    last_name = sms_data[1]
    student_email = sms_data[2]
    student_id = sms_data[3]
    student_password = sms_data[4]
    


    app.config['MAIL_USERNAME']= student_email

    msg = Message(subject='Login details...', recipients = [student_email])
    msg.body = "Hello {} {}, your email is confirmed, Your login details are >> student_id = {}, student_password = {}".format(first_name, last_name, student_id, student_password)
    mail.send(msg)

'''



@app.route('/confirm-email/<token>')
def confirm_email(token):
    try:
        student_email = t.loads(token, salt='email-confirm', max_age=86400)
    except SignatureExpired:
        return '<h1>The token is expired</h1>'
    '''
    print('Login details are ....!!!')
    first_name = _sms_data[0]
    last_name = _sms_data[1]
    student_email = _sms_data[2]
    student_id = _sms_data[3]
    student_password = _sms_data[4]

    msg = Message(subject='Login details...', recipients = [student_email])
    msg.body = "Hello {} {}, your email is confirmed, Your login details are >> student_id = {}, student_password = {}".format(first_name, last_name, student_id, student_password)
    mail.send(msg)
    '''

    return redirect(url_for('student_login'))        
 








@app.route('/logout')
@login_required
def logout():

    logout_user()
    msg = flash('You are now logged out....','success')

    return redirect(url_for('student_login', msg=msg))




@app.route('/faculty_registration', methods=['GET','POST'])
def faculty_registration():

    return render_template('faculty_registration.html')       








@app.route('/thankyou1')
@login_required
def thankyou1():
    
    return render_template('thankyou1.html')



@app.route('/thankyou2')
@login_required
def thankyou2():
    
    return render_template('thankyou2.html')



@app.route('/faculty_login')
def faculty_login():
    return render_template('faculty_login.html')          




@app.route('/student_dashboard')
@login_required
def student_dashboard():
    
    return render_template('student_dashboard.html')






@app.route('/student_all_videos')
@login_required
def student_all_videos():
    return render_template('student_all_videos.html')


@app.route('/student_update_profile')
@login_required
def student_update_profile():
    return render_template('student_update_profile.html')    


@app.route('/student_update_profile_picture')
@login_required
def student_update_profile_picture():
    return render_template('student_update_profile_picture.html')  




@app.errorhandler(400)
def error400(error):
    return '<h3>Serevr does not understand this request, Please go back to <a href="/">Home</a></h3>',400

@app.errorhandler(401)
def error401(error):
    return '<h3>You are not authorized to access this page , Please login first <a href="student_login">Login</a></h3>',401

@app.errorhandler(404)
def error404(error):
    return '<h3>Serevr does not understand this request, Please go back to <a href="/">Home</a></h3>',404

@app.errorhandler(408)
def error408(error):
    return '<h3>Request Time-out, Please go back to <a href="/">Home</a></h3>',408

@app.errorhandler(500)
def error500(error):
    return '<h3>Internal Server Problem, Please go back to <a href="/">Home</a></h3>',500                 

