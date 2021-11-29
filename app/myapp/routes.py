from myapp import myapp_obj
from myapp.forms import SignupForm, LoginForm
from flask import render_template, flash, redirect
from werkzeug.security import generate_password_hash

from myapp import db
from myapp.models import User
from flask_login import current_user, login_user, logout_user, login_required

@myapp_obj.route("/")
def home():
    return render_template("homepage.html")

@myapp_obj.route("/signup", methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(email = form.email.data, username = form.username.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("You can now login")
        return redirect("/")

    return render_template("signup.html", form = form)

@myapp_obj.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Login requested for user {form.username.data},remember_me={form.remember_me.data}')
            return redirect('/loggedin')
        else:
            flash("Login invalid username or password!")
            return redirect('/login')
    return render_template("login.html", form=form)

@myapp_obj.route("/loggedin")
@login_required
def log():
    return render_template("/loggedin.html")
@myapp_obj.route("/note/<int:user_id>", methods = ['GET', 'POST'])
@login_required
def note(user_id):
    """ Route to view a users notes"""
    postedNotes = []
    noteIndex = Notes.query.filter_by(User = user_id).all()

    if noteIndex is not None:
        for note in noteIndex:
            postedNotes = postedNotes + [{'Name':f'{note.name}','id':f'{note.id}'}]
        else:
            return redirect(url_for("myTodo"))
    return render_template('note.html', title = 'Notes', noteIndex = postedNotes, user_id = user_id)

@myapp_obj.route("/viewNote/<int:user_id>/<int:id>", methods = ['GET', 'POST'])
@login_required
def viewNotes(user_id, id):
    '''(not functional) route will allow for file to be opened and viewed in html '''
    note = Notes.query.filter_by(id=id).first()
    data = BytesIO(note.data).read()
    return render_template('view_note.html', title='Note', user_id=user_id, id=id, data=data)

@myapp_obj.route("/note2pdf/<int:id>", methods = ['GET', 'POST'])
@login_required
def note2pdf(id):
    '''(not functional) route will allow for html note to be downloaded as pdf '''
    note = Notes.query.filter_by(id=id).first()
    data = BytesIO(note.data).read()
    return render_template('pdfrender.html', title='Note', user_id=user_id, id=id, data=data)

@myapp_obj.route("/share_notes/<int:user_id>/<int:id>", methods = ['GET', 'POST'])
@login_required
def shareNote(user_id, id):




