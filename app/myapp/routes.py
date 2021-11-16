from myapp import myapp_obj
from myapp.forms import SignupForm
from flask import render_template, flash, redirect

from myapp import db
from myapp.models import User


@myapp_obj.route("/signup", methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You can now login")
        return redirect("/")

    return render_template("signup.html", form = form)

@myapp_obj.route("/")
def home():
    return render_template("homepage.html")