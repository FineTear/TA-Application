from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Courses, Apps

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('WSU Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    wsuid = StringField('WSU ID', validators=[DataRequired()])    
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    phonenumber = StringField('Phone Number (Digits Only)', validators=[DataRequired()])
    
    type = RadioField('Type', choices=[('student','Student'),('instructor','Instructor')],validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('The Email already Registered.')

class EditForm(FlaskForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    wsuid = StringField('WSU ID')
    phonenumber = StringField('Phone Number (Digits Only)')
    major = StringField('Major')
    gpa = FloatField('GPA')
    grad_date = StringField('Graduation Date')
    experience = StringField('Prior TA Experience')
    submit = SubmitField('Save')

class AddForm(FlaskForm):
	name = StringField(['Course'],validators=[DataRequired()])
	submit = SubmitField('Add')

class OpencloseForm(FlaskForm):
	name = StringField(['Course'],validators=[DataRequired()])
	choice = RadioField('Choice', choices=[('open','Open'),('closed','Closed')],validators=[DataRequired()])
	submit = SubmitField('Submit')

class AddremoveForm(FlaskForm):
	course = StringField(['Course'],validators=[DataRequired()])
	wsuid = StringField(['WSU_ID'],validators=[DataRequired()])
	choice = RadioField('Choice', choices=[('add','Add'),('remove','Remove')],validators=[DataRequired()])
	submit = SubmitField('Submit')

class DForm(FlaskForm):
	course = StringField(['Course'],validators=[DataRequired()])
	instructor = StringField(['Instructor'],validators=[DataRequired()])
	submit = SubmitField('Delete')

class AddAppForm(FlaskForm):
	name = StringField(['Course'],validators=[DataRequired()])
	instructor = StringField(['Instructor'],validators=[DataRequired()])
	grade = StringField(['Grade'],validators=[DataRequired()])
	datetaken = StringField(['Date_Taken'],validators=[DataRequired()])
	dateTA = StringField(['Date for TA'],validators=[DataRequired()])
	experience = RadioField('TA Experience', choices=[('yes','Yes'),('no','No')],validators=[DataRequired()])
	submit = SubmitField('Submit')
	
	def validate_name(self, name):
		course = Courses.query.filter_by(name=name.data).first() #,instructor = instructor.data
		if course.available != "open":
			raise ValidationError('Course is not open for applications.')