from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    type = db.Column(db.String(64), unique=False)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(64), unique=False)
    lastname = db.Column(db.String(120), unique=False)
    wsuid = db.Column(db.Integer, unique=False)
    phonenumber = db.Column(db.Integer, unique=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    assigned = db.Column(db.String(140), unique=False)
    course = db.Column(db.String(140), unique=False)
	
	
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
		
		
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=False)
    instructor = db.Column(db.String(140), unique=False)
    available = db.Column(db.String(140), unique=False)
    TAs = db.Column(db.String(200), unique=False)
	
    def __repr__(self):
        return '<Post {}>'.format(self.name)

class Apps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wsuid = db.Column(db.Integer, unique=False)
    course = db.Column(db.String(140), unique=False)
    instructor = db.Column(db.String(140), unique=False)
    grade = db.Column(db.String(5), unique=False)
    datetaken = db.Column(db.String(140), unique=False)
    dateTA = db.Column(db.String(140), unique=False)
    experience = db.Column(db.String(140), unique=False)
    accepted = db.Column(db.String(140), unique=False)
		
@login.user_loader
def load_user(id):
    return User.query.get(int(id))