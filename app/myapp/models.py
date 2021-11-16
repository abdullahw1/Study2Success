from myapp import db
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(128), unique = True)
    username = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(64))

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def __repr__(self):
        return f'<User {self.id}: {self.username}>'