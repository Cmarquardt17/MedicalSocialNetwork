from project import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    middleName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    dateOfBirth = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    ssn = db.Column(db.String(9), nullable=False)
    race = db.Column(db.String(20), nullable=False)
    emergency = db.Column(db.String(120), nullable=False)
    majorSurgery = db.Column(db.String(20), nullable=False)
    smoking = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}',\
                    '{self.firstName}', '{self.middleName}', '{self.lastName}',\
                    '{self.address}', '{self.phone}', '{self.dateOfBirth}',\
                    '{self.gender}', '{self.ssn}', '{self.race}',\
                    '{self.emergency}', '{self.majorSurgery}', '{self.smoking}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(100), nullable=False)
    medication = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.condition}', '{self.medication}', '{self.date_posted}')"
