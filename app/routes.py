from app import app,db,bcrypt, mail
from flask import render_template, url_for,request, flash, redirect, make_response
from app.models import User, Course, Question,Messages
from app.form import RegistrationForm, LoginForm, CourseForm, QuestionForm, RequestResetForm ,ResetPasswordForm,CoordinatorDetails, AnsuranceBoard, ApproveForm,PrintedForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import pdfkit


@app.route('/')
def index():
    return render_template('index.html')




@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
            user.set_user_role(form.user_role.data)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created', 'success')
            user1=User.query.filter_by(username=form.username.data).first()
            if user1.is_a_coordinator == True:
                return redirect(url_for('coordinator_update'))
            elif user1.is_assuranceboard == True:
                return redirect(url_for('assurance_update'))
            return redirect(url_for('login'))
        except:
            db.session.rollback()
        finally:
            db.session.close()
            
    return render_template('register.html', title='Register', form=form)

@app.route('/coordinator_update', methods=['GET','POST'])
def coordinator_update():
    form = CoordinatorDetails()
    if form.validate_on_submit():
        user  = User.query.filter_by(is_a_coordinator=True).order_by(User.date_created.desc()).first()
        user.courser_coordinator = form.coordinator_course.data
        db.session.commit()
        flash('Your have successfully updated your account', 'success')
        return redirect('login')
    return render_template('coordinator_update.html', form=form)



@app.route('/assurance_update', methods=['GET','POST'])
def assurance_update():
    form = AnsuranceBoard()
    if form.validate_on_submit():
        user  = User.query.filter_by(is_assuranceboard=True).order_by(User.date_created.desc()).first()
        user.courser_assurance_board = form.ansuranceboard_course.data
        db.session.commit()
        flash('Your have successfully updated all fields, Kindly Login', 'success')
        return redirect(url_for('login'))
    return render_template('assurance_update.html', form=form)

# @app.route('/role', methods=['GET','POST'])
# def role():
#     form = RoleForm()
#     if form.validate_on_submit():
#         user = User.query.
#         user = User()
#     flash('Your account has been created', 'success')
#     return render_template('role.html', form=form)
   


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if user.is_a_lecture:
                return redirect(next_page) if next_page else redirect(url_for('index'))
            # elif user.courser_coordinator == '':
            #     return redirect(next_page) if next_page else redirect(url_for('coordinator_update'))
            elif user.is_a_coordinator:
                return redirect(next_page) if next_page else redirect(url_for('coordinator'))
            # elif user.courser_assurance_board == '' :
            #     return redirect(next_page) if next_page else redirect(url_for('assurance_update'))
            elif user.is_assuranceboard:
                return redirect(next_page) if next_page else redirect(url_for('moderation_board'))
            elif user.is_a_staff_support:
                return redirect(next_page) if next_page else redirect(url_for('staff_support'))
        else:
            flash('Login unsuccessful, Please check your Email and Password', 'danger')
    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/quetion/create', methods=['GET','POST'])
@login_required
def create_question():
    form = QuestionForm()
    if form.validate_on_submit():
        try:
            course = Course.query.filter_by(user_id=current_user.id).first()
            question=Question(chapter=form.chapter.data, title=form.title.data, content=form.content.data, marks=form.marks.data, course_id=course.id)
            db.session.add(question)
            db.session.commit()
            flash('The Question has been created seccessfuly.','success')
            return redirect(url_for('find_question'))
        except:
            db.session.rollback()
        finally:
            db.session.close()
    return render_template('question.html', form=form)

@app.route('/find_question')
@login_required
def find_question():
    course = Course.query.filter_by(user_id=current_user.id).first()
    questions= Question.query.filter_by(course_id=course.id)
    return render_template('find_question.html', questions=questions, course=course)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        question = Question.query.get((id == form.id.data))
        question.content = request.form['content']
        question.marks = request.form['marks']
        db.session.commit()
        flash('question updated successfully', 'success')
        return redirect(url_for('find_question'))

@app.route('/check/<question_id>/set-completed', methods=['POST'])
def check(question_id):
    try:
        check = request.get_json()['check']
       
        question = Question.query.get(question_id)
        
        question.check = check 
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('find_question'))
    

@app.route('/preview')
def preview():
    questions = Question.query.filter_by(check=True).all()
    users = User.query.filter_by(is_assuranceboard=True)
    return render_template('preview.html', questions=questions, users=users)

@app.route('/for_review', methods=['POST'])
def for_review():
    try:
        message_to =request.form['message-to']
        user = User.query.filter_by(username=message_to).first()
        message= request.form['message']
        message1 = Messages(message=message, message_to=user.id)
        db.session.add(message1)
        db.session.commit()
        flash('You have successfuly submited your exam paper to ansurance board')
        return redirect(url_for('find_question'))
    except:
        db.session.close()
    finally:
        db.session.close()
    
    



@app.route('/course/create', methods=['GET','POST'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        try:
            course = Course(course_name=form.course_name.data, course_code=form.course_code.data, year = form.class_year.data, user_id=current_user.id)
            db.session.add(course)
            db.session.commit()
            flash(f'{form.course_name.data} has been created seccessfuly.','success')
            return redirect(url_for('find_course'))
        except:
            db.session.rollback 
        finally:
            db.session.close()
            
    return render_template('course.html', form=form)

@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    question = Question.query.get(id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully')

    return redirect(url_for('find_question'))

@app.route('/find_course')
@login_required
def find_course():
    courses = Course.query.filter_by(user_id=current_user.id).order_by(Course.date_posted.desc()).all()
    course = Course.query.filter_by(user_id=current_user.id).order_by(Course.date_posted.desc()).first()
    questions = Question.query.filter_by(course_id= course.id).order_by(Question.date_posted.desc()).first()
    return render_template('find_course.html', courses=courses, questions=questions)


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='karenkapambwe@gmail.com', recipients=[user.email])
    msg.body=f''' To reset your password, Visit the following link:
    {url_for('reset_token', token=token, _external=True)}
        
    If you did not make this request, simply ignore this email and no changes will be made
    '''
    mail.send(msg)


@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An Email has been sent with instructions to reset Your Password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title = 'Reset Password', form=form)



@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user.password=hashed_password
            db.session.commit()
            flash('Your Your Password has been updated, You are now able to Log In', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
        finally:
            db.session.close()
            
    return render_template('reset_token.html', title = 'Reset Password', form=form)


@app.route('/moderation_board', methods=['GET','POST'])
@login_required
def moderation_board():
    form = ApproveForm()
    if request.method=='POST':
        message_to= User.query.filter_by(username=request.form['name']).first()
        message = Messages(message=form.message.data, message_to= message_to.id )
        db.session.add(message)
        db.session.commit()
        flash('Message sent successful','success')
    messages = Messages.query.filter_by(message_to=current_user.id).all()
    user = User.query.filter_by(username=current_user.username).first()
    courses = user.courser_assurance_board
    course = Course.query.filter_by(course_name=courses).first()
    question = Question.query.filter_by(course_id=course.id).first()
    users = User.query.filter_by(is_a_coordinator=True)
    return render_template('moderation_board.html',form=form, messages = messages, courses=courses, question=question,  users=users)

@app.route('/moderator_review_view')
def moderator_review_view():
    questions = Question.query.filter_by(check=True).all()
    users = User.query.filter_by(is_a_coordinator=True)
    return render_template('moderator_review_view.html', questions = questions , users=users)

@app.route('/coordinator')
@login_required
def coordinator():
    messages = Messages.query.filter_by(message_to=current_user.id).all()
    user = User.query.filter_by(username=current_user.username).first()
    courses = user.courser_coordinator
    course = Course.query.filter_by(course_name=courses).first()
    question = Question.query.filter_by(course_id=course.id).first()
    return render_template('coordinator.html', messages = messages, courses=courses, question=question, title='Coordinator')

@app.route('/staff_support', methods=['GET','POST'])
@login_required
def staff_support():
    form = PrintedForm()
    if request.method=='POST':
        course = Course.query.filter_by(course_name=request.form['course']).order_by(Course.date_posted.desc()).first()
        question = Question.query.filter_by(course_id=course.id).first()
        data = form.printed .data
        if data == 'printed':
            question.printed_data =True
            db.session.commit()
        elif data=='not printed':
            question.printed_data=False 
            db.session.commit()
        flash('The status has been updated', 'success')
        return redirect(url_for('staff_support'))
    question = Question.query.filter_by(approved=True).order_by(Question.date_posted.desc()).first()
    course = question.courses.course_name 
    user_id = question.courses.user_id
    user1 = User.query.get(user_id)
    user = user1.username
    return render_template('staff_support.html', form=form, question=question, course=course, user=user)

@app.route('/staff_support_review_view')
def staff_support_review_view():
    questions = Question.query.filter_by(check=True).all()
    users = User.query.filter_by(is_a_coordinator=True)
    return render_template('staff_support_review_view.html', questions = questions , users=users)

@app.route('/to_pdf')
def to_pdf():
    questions = Question.query.filter_by(check=True).all()
    users = User.query.filter_by(is_a_coordinator=True)
    res = render_template('staff_support_review_view_pdf.html', questions = questions , users=users)
    response_string = pdfkit.from_string(res, False) 
    response = make_response(response_string)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition']='inline; filename=exam-paper.pdf'
    return response
    




@app.route('/review_view')
def review_view():
    questions = Question.query.filter_by(check=True).all()
    users = User.query.filter_by(is_a_coordinator=True)
    return render_template('review_view.html', questions = questions , users=users)

@app.route('/approved', methods=['GET','POST'])
def approved():
    form = ApproveForm()
    if request.method == 'POST':
        messages = Messages.query.filter_by(message_to=current_user.id).all()
        user = User.query.filter_by(username=current_user.username).first()
        courses = user.courser_coordinator
        
        course = Course.query.filter_by(course_name=courses).first()
        question = Question.query.filter_by(course_id=course.id).first()
        approved=form.approve.data
        if approved == 'Approved':
            data = True
            question.approved = data
            print(question.approved )
            db.session.commit()
        elif approved== 'Not Approved':
            data = False
            question.approved = data
            print(question.approved )
            db.session.commit()
        message_to= User.query.filter_by(username=request.form['name']).first()
        message = Messages(message=form.message.data, message_to= message_to.id )
        db.session.add(message)
        db.session.commit()
        flash('Message sent successful','success')
        return redirect(url_for('coordinator'))
    lectures = User.query.filter_by(is_a_lecture=True).all()
    return render_template('approved.html', form=form, lectures=lectures)