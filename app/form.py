from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextField, FileField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import User,Course
from flask_login import  current_user


class RegistrationForm(FlaskForm):
    username = StringField('Full Name', validators=[
                           DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    user_role = SelectField('Facult Role', choices=['Lecture', 'Assurance Board', 'Coordinator', 'staff support'])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken, Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken, Please choose a different one')


        
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    

class CourseForm(FlaskForm):
    course_name = SelectField('Course Name', choices=['Programming','Computer Systems','Software Engineering','Databases and Management Systems','Networks','information security','Advanced Databases','Algorithm and Data structure'])
    course_code = StringField('Course Code', validators=[DataRequired()])
    class_year = SelectField('Class Year', choices=['First Year', 'Second Year', 'Third Year', 'Fouth Year','Fifth Year'])
    submit = SubmitField('Create A Course')
    
    def validate_course_name(self, course_name):
        course = Course.query.filter_by(course_name=course_name.data).first()
        if course:
            raise ValidationError(
                'That course_name is taken, Please choose a different one')
    
    def validate_course_code (self, course_code ):
        course = Course.query.filter_by(course_code =course_code.data).first()
        if course:
            raise ValidationError(
                'That course_code  is taken, Please choose a different one')
   
   
def choices_query():
    user = User.query.filter_by(username=current_user.username).first()
    course = user.courses
    return course
    
    
class QuestionForm(FlaskForm):
    chapter = StringField('Chapter',validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    marks = StringField('Marks', validators=[DataRequired()])
    Atach_image = FileField('Atach an Image')
    submit = SubmitField('Create A Question')
    
    

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that Email, You must register first.')
            
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    
    
class CoordinatorDetails(FlaskForm):
    coordinator_course = SelectField('Which Course Do you coordinate',choices=['Programming','Computer Systems','Software Engineering','Databases and Management Systems','Networks','information security','Advanced Databases','Algorithm and Data structure'])
    submit = SubmitField('Next')

class AnsuranceBoard(FlaskForm):
    ansuranceboard_course = SelectField('Which Course Do you Review',choices=['Programming','Computer Systems','Software Engineering','Databases and Management Systems','Networks','information security','Advanced Databases','Algorithm and Data structure'])
    submit = SubmitField('Next')


class ApproveForm(FlaskForm):
    approve = SelectField('Status',choices=['Approved', 'Not Approved'])
    message = TextAreaField('Message' ,validators=[DataRequired()])
    message_to = SelectField('Message to',choices=[])
    submit = SubmitField('Submit')


class PrintedForm(FlaskForm):
    printed = SelectField('Printed', choices=['printed', 'not printed'])
    submit = SubmitField('Submit')

    
   
    