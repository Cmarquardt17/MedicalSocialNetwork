from project import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin
from flask import current_app

#Loads the user dynamically to the website with all of their information
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#The table of all of the available friends and potential friends
friends = db.Table('friends',
    db.Column('friend1_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('friend2_id', db.Integer, db.ForeignKey('user.id'))
)

#The information a user will put in for themselves when creating an account
#Friends will also be in this category where all information for that person is loaded up
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    middleName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    doctor = db.Column(db.String(10), nullable=False)
    drLicenseNum = db.Column(db.String(7), nullable=False)
    dateOfBirth = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    ssn = db.Column(db.String(9), nullable=False)
    race = db.Column(db.String(20), nullable=False)
    emergencyName = db.Column(db.String(120), nullable=False)
    emergencyRelation = db.Column(db.String(120), nullable=False)
    emergencyAddress = db.Column(db.String(120), nullable=False)
    emergencyPhone = db.Column(db.String(120), nullable=False)
    majorSurgery = db.Column(db.String(20), nullable=False)
    smoking = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    friended = db.relationship('User',
                            secondary=friends,
                            primaryjoin=(friends.c.friend1_id == id),
                            secondaryjoin=(friends.c.friend2_id == id),
                            backref=db.backref('friends', lazy='dynamic'),
                            lazy='dynamic')

    #If you are friends with that user you will see their posts
    def followed_posts(self):
        return Post.query.join(friends, (friends.c.friend2_id == Post.user_id)).filter(friends.c.friend1_id == self.id).order_by(Post.date_posted.desc())

    #Our friend function that appends a user to them as a friend
    def friend(self, user):
        if not self.is_friends(user):
            self.friended.append(user)
            return self

    #User also has the option to unfollow that person at any given time
    def unfriend(self, user):
        if self.is_friends(user):
            self.friended.remove(user)
            return self

    #Will display that user if you are friends with them, like a check
    def is_friends(self, user):
        return self.friended.filter(friends.c.friend2_id == user.id).count() > 0

    #For security matters
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    #This is a static method that doesn't change but resets the verify token for the specific user
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    #Used to compute the string representation of the user
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}',\
                    '{self.firstName}', '{self.middleName}', '{self.lastName}',\
                    '{self.address}', '{self.phone}', '{self.doctor}', '{self.drLicenseNum}'\
                    '{self.dateOfBirth}', '{self.gender}', '{self.ssn}', '{self.race}',\
                    '{self.emergencyName}', '{self.emergencyRelation}', '{self.emergencyAddress}',\
                    '{self.emergencyPhone}', '{self.majorSurgery}', '{self.smoking}','{self.confirmed}')"

#Our post method that entails everything a user can post or receive in their feed if they are 'friends'
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient = db.Column(db.String(100), nullable=True)
    condition = db.Column(db.String(100), nullable=False)
    medication = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #Similar to the one above, this compute the string for the post of the condition
    def __repr__(self):
        return f"Post('{self.patient}', '{self.condition}', '{self.medication}', '{self.date_posted}')"
