import enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from myapp import login 
from myapp import db

class FriendStatusEnum(enum.Enum):
    PENDING = 0
    FRIEND = 1

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Enum(FriendStatusEnum))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    flashcards = db.relationship('FlashCard', backref='user' , lazy='dynamic')
    friend1 = db.relationship('Friend', backref='user1' , lazy='dynamic', foreign_keys=[Friend.user1_id])
    friend2 = db.relationship('Friend', backref='user2' , lazy='dynamic', foreign_keys=[Friend.user2_id])

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.id}: {self.username}, {self.password}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class FlashCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.Text)
    back = db.Column(db.Text)
    learned = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<FlashCard {self.id}: {self.front}, {self.back}>'


# class CardProgress(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     progress = db.Column(db.Text)
#     index = db.Column(db.Integer)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
