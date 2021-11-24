from werkzeug.security import generate_password_hash
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from myapp import myapp_obj
from myapp.forms import SignupForm, LoginForm, FlashCardForm
from myapp import db
from myapp.models import User, FlashCard

@myapp_obj.route("/")
def home():
    return render_template("homepage.html")

@myapp_obj.route("/signup", methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("log"))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(email = form.email.data, username = form.username.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created. You can now login")
        return redirect(url_for("home"))

    return render_template("signup.html", form = form)

@myapp_obj.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("log"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Login requested for user {form.username.data},remember_me={form.remember_me.data}')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("log"))
        else:
            flash("Login invalid username or password!")
            return redirect('/login')
    return render_template("login.html", form=form)

@myapp_obj.route("/loggedin")
@login_required
def log():
    return render_template("/loggedin.html")

@myapp_obj.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@myapp_obj.route("/add-flashcard", methods = ['GET', 'POST'])
@login_required
def add_flashcard():
    form = FlashCardForm()
    if form.validate_on_submit():
        card = FlashCard(front = form.front.data, back = form.back.data, user = current_user._get_current_object())
        db.session.add(card)
        db.session.commit()
        flash("Flashcard has been created")
        return redirect(url_for("add_flashcard"))
    return render_template("/add-flashcard.html", form = form)

@myapp_obj.route("/pomodoro")
def pomodoro():
    return render_template("/pomodoro.html")
