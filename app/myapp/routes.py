import random
from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required

from myapp import myapp_obj
from myapp.forms import SignupForm, LoginForm, FlashCardForm, NextButton, PreviousButton, ObjectiveForm
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
        user = User(email=form.email.data, username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created. You can now login")
        return redirect(url_for("home"))

    return render_template("signup.html", form = form)

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("log"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
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

@myapp_obj.route("/add-flashcard", methods=['GET', 'POST'])
@login_required
def add_flashcard():
    form = FlashCardForm()
    if form.validate_on_submit():
        card = FlashCard(front=form.front.data, back=form.back.data, view=0, learned=0, user=current_user._get_current_object())
        db.session.add(card)
        db.session.commit()
        flash("Flashcard has been created")
        return redirect(url_for("add_flashcard"))
    return render_template("/add-flashcard.html", form=form)

@myapp_obj.route("/my-flashcard")
@login_required
def show_flashcard():
    # cards = FlashCard.query.filter_by(user_id = current_user.get_id()).all()
    ordered_cards = FlashCard.query.filter_by(user_id=current_user.get_id()).order_by(FlashCard.learned).all()
    if ordered_cards is None:
        flash("You don't have any flashcards. Please create one")
        return redirect(url_for("add_flashcard"))
    return render_template("my-flashcard.html", ordered_cards=ordered_cards)

def shuffle_choices(current_card, cards):
    numRow = len(cards) # number of flashcards that the current user has
    card_id = current_card.id
    numbers = list(range(1, numRow + 1)) # list(range(numRow))
    numbers.remove(card_id) # remove card_id from the list numbers
    random.shuffle(numbers) # shuffle the list numbers
    lst_id = []
    for i in range (3):
        temp = numbers.pop()
        lst_id.append(cards[temp-1].id)
    lst_id.append(card_id)
    random.shuffle(lst_id)
    return lst_id


@myapp_obj.route("/learn-flashcard", methods=['GET', 'POST'])
@login_required
def learn_flashcard():
    first_card = FlashCard.query.filter_by(user_id=current_user.get_id()).order_by(FlashCard.learned, FlashCard.view).first()
    cards = FlashCard.query.filter_by(user_id=current_user.get_id()).all() # list of cards that the current user has

    if len(cards) < 4:
        flash("You must have at least 4 flashcards. Please create more flashcards")
        return redirect(url_for("add_flashcard"))
    
    form = ObjectiveForm()
    formNext = NextButton()
    list_id = shuffle_choices(first_card, cards)
    choice = [FlashCard.query.get(x) for x in list_id]



    if form.validate_on_submit():
        if form.A.data:
            if form.A.raw_data[0] == first_card.back:
                flash('Excellent')
                first_card.learned += 1
                db.session.commit()
            else:
                flash('opps. Wrong answer')
        elif form.B.data:
            if form.B.raw_data[0] == first_card.back:
                first_card.learned += 1
                db.session.commit()
                flash('Excellent')
            else:
                flash('opps. Wrong answer')
        elif form.C.data:
            if form.C.raw_data[0] == first_card.back:
                flash('Excellent')
                first_card.learned += 1
                db.session.commit()
            else:
                flash('opps. Wrong answer')
        elif form.D.data:
            if form.D.raw_data[0] == first_card.back:
                flash('Excellent')
                first_card.learned += 1
                db.session.commit()
            else:
                flash('opps. Wrong answer')
    else:
        if formNext.validate_on_submit():
            flash("hello")
            first_card.view += 1
            db.session.commit()
            return redirect(url_for("learn_flashcard"))

    form.A.label.text = choice[0].back
    form.B.label.text = choice[1].back
    form.C.label.text = choice[2].back
    form.D.label.text = choice[3].back
    return render_template("learn-flashcard.html", first_card=first_card, form=form, formNext=formNext, choice=choice, list_id=list_id)

