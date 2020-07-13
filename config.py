from app import app

DEBUG=True

'''
#SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/mysqldb'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_CURSORCLASS'] ='DictCursor'
#app.config['MYSQL_DB'] = 'mysqldb'
app.config['MYSQL_DB'] = 'maiic_video_conference_details'
'''

#SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:mysql2020@localhost/maiic3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False








'''
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'maiiceducate@gmail.com'
app.config['MAIL_PASSWORD'] = 'medu12345'
app.config['MAIL_DEFAULT_SENDER'] =('MAIIC.Edu.IT','maiiceducate@gmail.com')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

'''
app.config['MAIL_SERVER']='smtpout.secureserver.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'enquiry@maiiceducation.com'
app.config['MAIL_PASSWORD'] = 'Enquiry@123'
app.config['MAIL_DEFAULT_SENDER'] =('MAIIC.Edu.IT','enquiry@maiiceducation.com')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



SECRET_KEY = 'thisissecretkey'