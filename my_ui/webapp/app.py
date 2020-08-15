import os, sys, uuid, datetime, json, logging, requests, pdb
from datetime import timedelta

import flask
from flask import Flask, request, session, redirect, jsonify, make_response, send_from_directory, render_template, url_for, flash, send_file, Response
from mimetypes import MimeTypes
from tempfile import mkdtemp

from flask_paginate import Pagination, get_page_parameter

from flask_cors import CORS, cross_origin

from werkzeug import serving
from werkzeug.datastructures import FileStorage
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

from forms import VideoUploadForm

logging.basicConfig(filename='logs/maiic_api_logs.log', format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('logs/maiic_api_logs.log')
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
CORS(app)

api_base_url = os.getenv('API_BASE_URL', 'http://localhost:3000/v1')
app.secret_key = "secret_key"
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

@app.before_request
def make_session_permanent():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(minutes=59)

@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
	if request.method == 'GET':
		return render_template('student_registration.html')
	if request.method == 'POST':
		firstName = request.form.get('firstName')
		lastName = request.form.get('lastName')
		email = request.form.get('email')
		alternet_email = request.form.get('alternet_email')
		mobile = request.form.get('mobile')
		city = request.form.get('city')
		class_standard = request.form.get('class_standard')

		subj = request.form.getlist('subject')
		print(subj)
		subject = ','.join(subj)
		print(subject)

		edu_board = request.form.get('edu_board')

		params = {"firstName" : firstName, "lastName":lastName, "email" : email, "alternet_email" : alternet_email,"mobile" : mobile, "city":city, "class_standard" : class_standard,"subject":subject, "edu_board" : edu_board }

		headers = {"Content-type": "application/json"}

		resp = requests.post(api_base_url + "/registration/",
								 data=json.dumps(params), headers=headers)

		res = resp.json()
		print("res.....",res)
		print("resp...",resp)
		if resp.status_code == 409:
			msg = flash('Email already exixts, please choose another one.','danger')
			return redirect(url_for('student_signup', msg=msg))
		if resp.status_code == 201:
			msg = flash('Successfully registered, please check mail for login details.','success')
			return redirect(url_for('student_login', msg=msg))

@app.route('/faculty_signup', methods=['GET', 'POST'])
def faculty_signup():
	if request.method == 'GET':
		return render_template('faculty_registration.html')
	if request.method == 'POST':
		firstName = request.form.get('firstName')
		lastName = request.form.get('lastName')
		email = request.form.get('email')
		alternet_email = request.form.get('alternet_email')
		mobile = request.form.get('mobile')
		city = request.form.get('city')
		class_standard = request.form.get('class_standard')
		subject = request.form.get('subject')
		edu_board = request.form.get('edu_board')

		params = {"firstName" : firstName, "lastName":lastName, "email" : email, "alternet_email" : alternet_email,"mobile" : mobile, "city":city, "class_standard" : class_standard, "subject" : subject, "edu_board" : edu_board }

		headers = {"X-Faculty" : "userAsFaculty", "Content-type": "application/json"}

		resp = requests.post(api_base_url + "/registration/",
								 data=json.dumps(params), headers=headers)

		res = resp.json()
		if resp.status_code == 409:
			msg = flash('Email already exists, please choose another one.','danger')
			return redirect(url_for('faculty_signup', msg=msg))
		if resp.status_code == 201:
			msg = flash('Successfully registered.','success')
			return redirect(url_for('faculty_login',msg=msg))

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
	if request.method == 'GET':
		return render_template('student_login.html')
	if request.method == 'POST':
		user_id = request.form.get('user_id')
		password = request.form.get('password')

		params = {"user_id":user_id, "password":password}
		headers = {"Content-type": "application/json"}

		resp = requests.post(api_base_url + "/login/",
							 data=json.dumps(params), headers=headers)

		res = resp.json()
		print(res)
		print(res)
		if resp.status_code == 401:
			msg = flash("Invalid credential","danger")
			return render_template("student_login.html",msg=msg)
		if resp.status_code == 409:
			msg = flash("Username or Password does not found","danger")
			return render_template("student_login.html", msg=msg)

		if resp.status_code == 200:
			session['token'] = res['token']
			session['role'] = res['role']
			session['email'] = res['email']
			#msg = flash("Successfully logged in","success")
			return redirect(url_for('students_dashboard'))






@app.route('/faculty_login', methods=['GET', 'POST'])
def faculty_login():
	if request.method == 'GET':
		return render_template('faculty_login.html')
	if request.method == 'POST':
		user_id = request.form.get('user_id')
		password = request.form.get('password')

		params = {"user_id":user_id, "password":password}
		headers = {"X-Faculty" : "userAsFaculty", "Content-type": "application/json"}

		resp = requests.post(api_base_url + "/login/",
								 data=json.dumps(params), headers=headers)

		res = resp.json()
		if resp.status_code == 401:
			msg = flash("Invalid credential","danger")
			return render_template("faculty_login.html",msg=msg)
		if resp.status_code == 409:
			msg = flash("Username or Password does not found","danger")
			return render_template("faculty_login.html",msg=msg)
		if resp.status_code == 200:
			session['token'] = res['token']
			session['role'] = res['role']
			session['email'] = res['email']
			#msg = flash("Successfully logged in.","success")
			return redirect(url_for('faculty_dashboard'))


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
	if request.method == 'GET':
		return render_template('admin_login.html')
	if request.method == 'POST':
		user_id = request.form.get('user_id')
		password = request.form.get('password')

		params = {"user_id":user_id, "password":password}
		headers = {"X-Admin" : "userAsAdmin", "Content-type": "application/json"}

		resp = requests.post(api_base_url + "/admin_login/",
								 data=json.dumps(params), headers=headers)

		res = resp.json()
		if resp.status_code == 401:
			msg = flash("Invalid credential","danger")
			return render_template("admin_login.html",msg=msg)
		if resp.status_code == 409:
			msg = flash("Username or Password does not found","danger")
			return render_template("admin_login.html",msg=msg)
		if resp.status_code == 200:
			session['token'] = res['token']
			session['role'] = res['role']
			session['email'] = res['email']
			#msg = flash("Successfully logged in.","success")
			return redirect(url_for('admin_dashboard'))



@app.route('/logout')
def logout():
	session.pop('token', None)
	session.pop('email',None)
	return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():	
	# if not session.get("token") is None:
	return render_template('index.html')
	# else:
	# 	flash("not permitted this page!")
	# 	return redirect(url_for("login")) 
'''
@app.route('/students_dashboard', methods=['GET'])
def students_dashboard():
	if not session.get("token") is None:
		if request.method == "GET":
			headers = {"x-access-token": session["token"]}
			resp = requests.get(api_base_url+"/get_videos",headers=headers)
			videos = resp.json()
			print(videos)
			return render_template("students_dashboard.html", videos = videos)
		return render_template("students_dashboard.html")
		
	else:
		msg = flash("You have to login first, for accessing this page.","danger")
		return redirect(url_for("student_login", msg=msg))
'''

@app.route('/students_dashboard')
def students_dashboard():
	if not session.get("token") is None:
		return render_template('students_dashboard.html')
	return redirect(url_for('student_login'))

@app.route('/admin_dashboard')
def admin_dashboard():
	if not session.get("token") is None:
		return render_template('admin_dashboard.html')
	return redirect(url_for('admin_login'))

'''
@app.route('/faculty_dashboard', methods=['GET'])
def faculty_dashboard():
	
	if not session.get("token") is None:
		headers = {"x-access-token" : session["token"]}
		videos = requests.get(api_base_url+"/videos", headers=headers)
		videos_data = videos.json()

		if videos_data:
			return render_template('faculty_dashboard.html', videos=videos_data['videos'])
	else:
		msg = flash("You have to login first, for accessing this page.","danger")
		return redirect(url_for("faculty_login", msg=msg))
'''
@app.route('/faculty_dashboard')
def faculty_dashboard():
	return render_template('faculty_dashboard.html')


@app.route('/users', methods=['GET'])
def fetch_users():
	if (not session['token'] is None) and (session.get("role") in ['admin']):
		pass

@app.route('/upload_videos', methods=['GET'])
def upload_videos():
	if (not session['token'] is None) and (session.get("role") in ['faculty', 'admin']):
		form = VideoUploadForm()
		if form.validate_on_submit():
			subject = form.subject.data
			standard = form.standard.data
			chapter = form.chapter.data
			videoUrl = form.videoUrl.data
			selectFile = form.selectFile.data

			return redirect(url_for('upload_file'))
		return render_template('upload_video.html', form=form)

@app.route('/videos', methods=['GET','POST'])
def upload_file():
	if not session.get("token") is None:
		if request.method == 'GET':
			headers = {"x-access-token" : session["token"]}
			videos = requests.get(api_base_url+"/videos", headers=headers)
			videos_data = videos.json()

			if videos_data:
				return render_template('faculty_dashboard.html', videos=videos_data['videos'])
		
		if request.method == 'POST':
			subject = request.form.get('subject')
			standard = request.form.get('standard')
			chapter = request.form.get('chapter')
			videoUrl = request.form.get('videoUrl')

			params = {"subject":subject,"class_standard": standard,"chapter": chapter,"video_url":videoUrl}

			headers = {"X-Faculty" : "userAsFaculty", "x-access-token": session["token"]}

			if request.files["file"]:
				
				file = request.files["file"]

				videoFileName = secure_filename(file.filename)
				print(videoFileName)
				cwd = os.getcwd()+'/'
				if 'temp' not in os.listdir(cwd):
					os.mkdir(cwd + 'temp')
				if videoFileName != None:
					file.save(os.path.join(cwd + 'temp', videoFileName))
			
				with open(cwd + 'temp/'+ videoFileName, 'rb') as f:
					data_file = ImmutableMultiDict([("file", f)])
					resp = requests.post(api_base_url + "/videos", files=data_file, data=params, headers=headers)
			else:
				resp = requests.post(api_base_url + "/videos", data=params, headers=headers)
				print(resp)
			if resp.status_code == 201:
				msg = flash('Successfully uploaded','success')
				return render_template('faculty_dashboard.html',msg=msg)
	else:
		flash("not permitted this page!")
		return redirect(url_for("faculty_login"))

@app.route('/contact', methods=["GET","POST"])
def contact():
	return render_template('contact.html')

#@app.route('/feedbacks')
#def feedbacks():
#	return render_template('feedbacks.html')


@app.route('/courses')
def courses():
	return render_template('courses.html')


@app.route('/student_profile')
def student_profile():

	return render_template('student_profile.html')




'''
@app.route('/all_videos', methods=["GET"])
def all_videos():

	if request.method=="POST":
		return render_template('students_dashboard.html')
	if request.method == "GET":
		headers = {"Content-type":"application/json"}
		resp = requests.get(api_base_url + "/get_videos",headers=headers)
		
		video_data = resp.json()
		print(video_data)
		return render_template('students_dashboard.html', video_data= video_data['video_list'])
	return render_template('students_dashboard.html')	
'''

@app.route('/get_users', methods=["GET"])
def get_users():
	#if (not session['token'] is None) and (session.get("role") in ['admin']):

	if request.method == "POST":
		return render_template('get_users.html')
	if request.method == "GET":
		headers = {"x-access-token": session["token"]}
		resp = requests.get(api_base_url + "/get_users", headers=headers)

		users = resp.json()

		return render_template('get_users.html', users = users)
	return render_template('get_users.html')		

@app.route('/get_videos', methods=["GET"])
def get_videos():
	#if (not session['token'] is None) and (session.get("role") in ['admin']):

	if request.method == "POST":
		return render_template('get_videos.html')
	if request.method == "GET":
		headers = {"x-access-token": session["token"]}
		resp = requests.get(api_base_url + "/get_videos", headers=headers)

		videos = resp.json()

		return render_template('get_videos.html', videos = videos)
	return render_template('get_videos.html')	








@app.route('/forgot_password', methods=["POST","GET"])
def forgot_password():
	if request.method == "GET":
		return render_template("forgot_password.html")
	if request.method == "POST":
	
		email = request.form.get('email')
		print(email)
		headers = {"Content-type": 'application/json'}
		params = {'email':email}	
		resp = requests.post(api_base_url + "/forgot_password",
								 data=json.dumps(params), headers=headers)

		res = resp.json()
		#print(res)
		if resp.status_code == 201:
			msg = flash("User ID and Password reset successful, please check mail for login details","success")
			return render_template("student_login.html", msg=msg)
		if resp.status_code == 409:
			msg = flash("Email id not found, please enter registered Email id","danger")
			return render_template("forgot_password.html",msg=msg)

@app.route('/update_users', methods=['POST'])
def update_users():
	if request.method == "GET":
		return render_template('update_users.html')
	if request.method == "POST":
		u_id = request.form.get('u_id')
		print(u_id)
		email = request.form.get('email')
		
		password = request.form.get('password')
		print(password)
		payment_status = request.form.get('payment_status')
		print(payment_status)
	
		headers = {"x-access-token": session["token"]}
		params = {'u_id':u_id,'email':email,'password':password,'payment_status':payment_status}	
		resp = requests.post(api_base_url + "/update_users",
								 data=json.dumps(params), headers=headers)

		res = resp.json()
		print(res)
		if resp.status_code == 201:
			msg = flash('User Update Successful. ','success')
			return render_template('get_users.html', msg=msg)
		if resp.status_code == 409:
			msg = flash('Falied to update users data','danger')
			return render_template('get_users.html', msg=msg)							 




'''

@app.errorhandler(500)
def internal_server_error(error):
	app.logger.error('Server Error: %s', (error))
	return render_template('500.html'), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
	app.logger.error('Unhandled Exception: %s', (e))
	return render_template('500.html'), 500

@app.errorhandler(404)
def error404(error):
   return render_template('error404.html')

'''
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=3011)