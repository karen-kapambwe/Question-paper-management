from datetime import datetime
from itsdangerous import  TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, index = True)
    email = db.Column(db.String(25), unique=True , index = True)
    is_a_lecture = db.Column(db.Boolean, default=False)
    is_a_coordinator = db.Column(db.Boolean, default=False)
    is_assuranceboard = db.Column(db.Boolean, default=False)
    is_a_staff_support = db.Column(db.Boolean, default=False)
    courser_coordinator = db.Column(db.String())
    courser_assurance_board = db.Column(db.String())
    date_created = db.Column(db.DateTime,
                            default=datetime.utcnow, index=True)
    password = db.Column(db.String(25))
    image_picture = db.Column(db.String(25), default='default.jpg')
    courses = db.relationship('Course', backref='author',lazy=True)
    message = db.relationship('Messages', backref='message_by',lazy=True)
   

    
    def set_user_role(self, user_role):
        if user_role == 'Lecture':
            self.is_a_lecture = True 
        elif user_role == 'Coordinator':
            self.is_a_coordinator=True 
        elif user_role == 'Assurance Board':
            self.is_assuranceboard=True 
        elif user_role == 'staff support':
            self.is_a_staff_support=True




    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    @staticmethod                 
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id =  s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    
    def __repr__(self):
        return f"<User id:{self.id}, username:{self.username},email:{self.email}>"

class Course(db.Model):
    __tablename__='course'
    id=db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(), unique=True, index = True)
    course_code = db.Column(db.String(), unique=True, index = True)
    year = db.Column(db.String())
    date_posted = db.Column(db.DateTime,
                            default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    questions = db.relationship('Question', backref='courses', lazy=True)
    

    def __repr__(self):
        return f"<Course id:{self.id},course_name:{self.course_name},course_code:{self.course_code},year:{self.year}>"

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, index=True)
    message_to = db.Column(db.ForeignKey('user.id'), index=True)



class Question(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer,primary_key=True)
    chapter = db.Column(db.String(), index = True)
    title = db.Column(db.String(), index = True)
    content = db.Column(db.Text, index = True)
    answer = db.Column(db.Text , index = True)
    marks=db.Column(db.String(20), index = True)
    image_picture = db.Column(db.String(25), default='default.jpg')
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'))
    check = db.Column(db.Boolean, default=False)
    sections = db.Column(db.String(), index=True)
    approved = db.Column(db.Boolean, default=False)
    printed_data = db.Column(db.Boolean, default= False, index=True)


    def set_approved(self, approved):
        if approved == 'Approved':
            self.approved= True 
        elif approved == 'Not Approved':
            self.approved=False
        

   

    def __repr__(self):
        return f"<Course id:{self.id},chapter:{self.chapter},title:{self.title},marks:{self.marks}>"

   
    

        