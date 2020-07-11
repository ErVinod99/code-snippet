from app import *
import datetime
from flask_login import UserMixin
from app import ModelView, admin

@login_manager.user_loader
def load_user(id):
    return Students_data.query.get(int(id))



class Students_data(db.Model, UserMixin):
    __tablename__="students_data"
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    student_email = db.Column(db.String(50))
    parent_email = db.Column(db.String(50))
    student_phone_number = db.Column(db.String(50))
    parent_phone_number = db.Column(db.String(50))
    city = db.Column(db.String(50))
    standard = db.Column(db.String(50))
    current_address = db.Column(db.String(50))
    board = db.Column(db.String(50))
    subjects = db.Column(db.String(50))
    student_password= db.Column(db.String(60))
    date_created = db.Column(db.DateTime, default= datetime.datetime.utcnow)
    payment_status = db.Column(db.Boolean, default = False)
    #is_admin = db.Column(db.Boolean, default=True)

    def __init__(self, student_id,first_name,last_name,student_email,parent_email,student_phone_number,parent_phone_number,city,standard,current_address,board,subjects,student_password):
        self.student_id= student_id
        self.first_name=first_name
        self.last_name=last_name
        self.student_email=student_email
        self.parent_email=parent_email
        self.student_phone_number=student_phone_number
        self.parent_phone_number=parent_phone_number
        self.city=city
        self.standard=standard
        self.current_address=current_address
        self.board=board
        self.subjects=subjects
        self.student_password=student_password
        

'''
class admin_controller(ModelView):
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated    
        else:
            return abort
            

    def not_auth(self):
        return '<h3>You are not authrized to use the "Admin Dashboard", Back toto <a href="/">Home</a></h3></h3>'      



admin.add_view(admin_controller(Students_data, db.session))
'''

admin.add_view(ModelView(Students_data, db.session))


