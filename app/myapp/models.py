from myapp import db
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from myapp import login 

class User(UserMixin, db.Model):
   
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(128), unique = True)
    username = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(64))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.id}: {self.username}, {self.password}>'
  

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
   

   
class Notes(db.Model):
    """Database table for notes

     Attributes:
         id: Primary key
         title: String column, title of note
         data: text column, containing files data
         User: id if user who added notes
     """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    data = db.Column(db.Text)
    User = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return f'<{self.name}   {self.data}>'
