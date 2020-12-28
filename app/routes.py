from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from app.models import Courses
from app.models import Apps
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from app.forms import EditForm
from app.forms import AddForm
from app.forms import AddAppForm
from app.forms import DForm
from app.forms import OpencloseForm
from app.forms import AddremoveForm
import logging

@app.route('/')

@app.route('/add_application', methods=['GET', 'POST'])
@login_required
def add_application():	
	form = AddAppForm()
	user = current_user
	course = Courses.query.filter_by(available="open").all()
	
	if form.validate_on_submit():
		app = Apps(wsuid=current_user.wsuid, course= form.name.data, instructor = form.instructor.data, grade = form.grade.data, datetaken = form.datetaken.data, dateTA = form.dateTA.data, experience=form.experience.data,accepted = "no")
		db.session.add(app)
		db.session.commit()
		return redirect(url_for('student_main'))
	
	return render_template("add_application.html", title='add_application_page', form=form, course = course)

@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():	
	form = AddForm()
	user = current_user
	if form.validate_on_submit():
		course = Courses(name=form.name.data, instructor = user.lastname, available = "open")
		db.session.add(course)
		db.session.commit()
		return redirect(url_for('course'))
	return render_template("add_course.html", title='add_courses_page', form=form)

@app.route('/add_remove_student', methods=['GET', 'POST'])
@login_required
def add_remove_student():	
	form = AddremoveForm()
	user = current_user
	apps4me = Apps.query.filter_by(instructor=user.lastname,accepted='no').all()
	appsdone = Apps.query.filter_by(instructor=user.lastname,accepted='yes').all()
	course = Courses.query.filter_by(instructor=user.lastname, name = form.course.data).first()
	if form.validate_on_submit():
		if form.choice.data == "add":
			Uapp=Apps.query.filter_by(instructor=user.lastname,wsuid=form.wsuid.data,accepted='no').first()
			Uapp.accepted = "yes"
			if course.TAs == None:
				course.TAs = form.wsuid.data
			else: course.TAs = course.TAs + '|' +str(user.wsuid)
		elif form.choice.data == "remove":
			Uapp=Apps.query.filter_by(instructor=user.lastname,wsuid=form.wsuid.data,accepted='yes').first()
			Uapp.accepted = "no"
			TAList=course.TAs.split('|')
			app.logger.warning(TAList)
			
			TAList.remove(form.wsuid.data)
			app.logger.warning(TAList)
			if TAList == []:
				app.logger.warning("if")
				course.TAs = None
			else:
				app.logger.warning("for loop")
				for i in TAList:
					if course.TAs == None:
						course.TAs = i
					else: course.TAs = course.TAs + '|' +i
		app.logger.warning(course.TAs)
		db.session.commit()
		return redirect(url_for('instructor_main'))
	
	return render_template("add_remove_student.html", title='add_remove_student_page', form=form, course=course, apps4me=apps4me, appsdone=appsdone)

@app.route('/course', methods=['GET', 'POST'])
def course():
	user = current_user
	course = Courses.query.filter_by(instructor=user.lastname).all()
	
	return render_template('course.html', title = 'Course', course = course,)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    type = form.type.data,
                    wsuid=form.wsuid.data,
                    firstname=form.firstname.data, 
                    lastname=form.lastname.data, 
                    phonenumber=form.phonenumber.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        if user.type == "student":
            return redirect(url_for('student_main'))
        
        if user.type == "instructor":
            return redirect(url_for('instructor_main'))

    return render_template('create_account.html', title = 'Create Account', form = form)

@app.route('/edit_instructor', methods=['GET', 'POST'])
@login_required
def edit_instructor():	
	form = EditForm()
	user=current_user
	if request.method == 'GET':
		form.firstname.data = user.firstname
		form.lastname.data = user.lastname
		form.wsuid.data = user.wsuid
		#form.phonenumber = user.phonenumber //not able to call done know why

	if form.validate_on_submit():
		user = current_user
		user.firstname=form.firstname.data
		user.lastname=form.lastname.data
		user.wsuid=form.wsuid.data
		user.phonenumber=form.phonenumber.data
		db.session.commit()
		return redirect(url_for('instructor_main'))
	
	return render_template("edit_instructor.html", title='Instructor_edit_page', form=form)

@app.route('/edit_student', methods=['GET', 'POST'])
@login_required
def edit_student():	
	form = EditForm()
	user = current_user
	if request.method == 'GET':
		form.firstname.data = user.firstname
		form.lastname.data = user.lastname
		form.wsuid.data = user.wsuid
		#form.phonenumber = user.phonenumber //not able to call done know why
	
	if form.validate_on_submit():
		user = current_user
		user.firstname=form.firstname.data
		user.lastname=form.lastname.data
		user.wsuid=form.wsuid.data
		user.phonenumber=form.phonenumber.data
		user.gpa=form.gpa.data
		user.major=form.major.data
		user.grad_date=form.grad_date.data
		user.experience=form.experience.data
		db.session.commit()
		return redirect(url_for('student_main'))
	
	return render_template("edit_student.html", title='edit_Student_page', form=form)

@app.route('/instructor_assignment', methods=['GET', 'POST'])
@login_required
def instructor_assignment():
	user = current_user
	apps4me = Apps.query.filter_by(instructor=user.lastname,accepted='no').all()
	appsdone = Apps.query.filter_by(instructor=user.lastname,accepted='yes').all()
	for c in apps4me:
		userApps = Apps.query.filter_by(wsuid=c.wsuid).all()
		for r in userApps:
			if r.accepted == "yes":
				apps4me.delete(c)

	return render_template("instructor_assignment.html", title='Instructor_assignment_page', apps4me=apps4me, appsdone=appsdone)

@app.route('/instructor_main', methods=['GET', 'POST'])
@login_required
def instructor_main():
	user = current_user

	return render_template("instructor_main.html", title='Instructor_main_page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if request.referrer == None:
            if current_user.type == "student":
                return redirect(url_for('student_main'))
            if current_user.type == "instructor":
                return redirect(url_for('instructor_main'))
        else:
            return redirect(request.referrer)

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid WSU Eamil or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        if user.type == "student":
            return redirect(url_for('student_main'))
        if user.type == "instructor":
            return redirect(url_for('instructor_main'))
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid WSU Email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('login')
        return redirect(next_page)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/open_close_course', methods=['GET', 'POST'])
@login_required
def open_close_course():	
	form = OpencloseForm()
	user = current_user
	course = Courses.query.filter_by(instructor=user.lastname).all()
	if form.validate_on_submit():
		Courses.query.filter_by(name=form.name.data, instructor = user.lastname).first().available = form.choice.data 
		db.session.commit()
		return redirect(url_for('instructor_main'))
	return render_template("open_close_course.html", title='open_close_course_page', form=form, course=course)	

@app.route('/remove_application', methods=['GET', 'POST','DELETE'])
@login_required
def remove_application():	
	form = DForm()
	user = current_user
	myapps = Apps.query.filter_by(wsuid=user.wsuid,accepted='no').all()
	
	if form.validate_on_submit():
		removeapp = Apps.query.filter_by(wsuid=user.wsuid,course = form.course.data, instructor = form.instructor.data ,accepted='no').first()
		db.session.delete(removeapp)
		db.session.commit()
		return redirect(url_for('student_main'))
	return render_template("remove_application.html", title='remove_application_page', form=form, myapps = myapps)

@app.route('/student_assignment', methods=['GET', 'POST'])
@login_required
def student_assignment():	
	user = current_user
	course = Courses.query.filter_by(available="open").all()
	myapps = Apps.query.filter_by(wsuid=user.wsuid,accepted='no').all()
	Aapp = Apps.query.filter_by(wsuid=user.wsuid,accepted="yes").first()
	
	return render_template("student_assignment.html", title='Student_assignment_page', course = course, myapps = myapps, Aapp=Aapp)

@app.route('/student_main', methods=['GET', 'POST'])
@login_required
def student_main():	
	user = current_user

	return render_template("student_main.html", title='Student_page')