from flask import render_template, flash, redirect, url_for, request, jsonify, abort
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required

from myapp import myapp_obj
from myapp.forms import SignupForm, LoginForm, FlashCardForm, UploadMarkdownForm, SearchForm
from myapp import db
from myapp.models import User, FlashCard, Friend, FriendStatusEnum
from myapp.models import get_friend_status
from myapp.mdparser import md2flashcard

@myapp_obj.route("/")
def home():
    return render_template("homepage.html")

@myapp_obj.route("/signup", methods=['GET', 'POST'])
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

    return render_template("signup.html", form=form)

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
    return render_template("/homepage.html")

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
        card = FlashCard(front=form.front.data, back=form.back.data, learned=0, user=current_user._get_current_object())
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


@myapp_obj.route("/import-flashcard", methods=['GET', 'POST'])
@login_required
def import_flashcard():
    form = UploadMarkdownForm()
    if form.validate_on_submit():
        f = form.file.data
        content = f.stream.read().decode('ascii')
        for section, flashcards in md2flashcard(content).items(): # TODO: Save flashcard by section
            for flashcard in flashcards:
                card = FlashCard(front=flashcard.front, back=flashcard.back, learned=0,  user=current_user._get_current_object())
                db.session.add(card)
        db.session.commit()
        flash(f'Uploaded file {f.filename} into flashcards')
        return redirect(url_for("show_flashcard"))
    return render_template("import-flashcard.html", form=form)


@myapp_obj.route("/my-friends", methods=['GET', 'POST'])
@login_required
def show_friends():
    friends = []
    result = db.session.query(Friend)\
                .filter((Friend.user1_id == current_user.get_id())\
                        | (Friend.user2_id == current_user.get_id())
                ).all()
    for x in result:
        if x.user1.id == int(current_user.get_id()):
            cur_user = x.user1
            oth_user = x.user2
        else:
            cur_user = x.user2
            oth_user = x.user1
        if x.status == FriendStatusEnum.FRIEND:
            buttons = [(f'/remove-friend/{oth_user.id}', 'Remove Friend')]
        elif x.status == FriendStatusEnum.PENDING:
            if cur_user is x.user1: # Current user sent the request
                buttons = [(f'/remove-friend/{oth_user.id}', 'Unsend')]
            else: # Other user sent the request
                buttons = [(f'/add-friend/{oth_user.id}', 'Approve'), (f'/remove-friend/{oth_user.id}', 'Reject')]
        else:
            abort(404, f'Unknown status {x.status}')
        friends.append((oth_user, x.status, buttons))
    return render_template("my-friends.html", friends=friends)


@myapp_obj.route("/add-friend", methods=['GET', 'POST'])
@login_required
def add_friend():
    found_users = []
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_str = search_form.text.data
        result = User.query.filter(User.username.contains(search_str) & (User.id != (current_user.get_id()))).all()
        for user in result:
            status, _ = get_friend_status(current_user.get_id(), user.id)
            if status == 'friend':
                buttons = [(f'/remove-friend/{user.id}', 'Remove Friend')]
            elif status == 'pending-sent-request':
                buttons = [(f'/remove-friend/{user.id}', 'Unsend')]
            elif status == 'pending-to-approve':
                buttons = [(f'/add-friend/{user.id}', 'Approve'), (f'/remove-friend/{user.id}', 'Reject')]
            elif status == 'neutral':
                buttons = [(f'/add-friend/{user.id}', 'Add Friend')]
            else:
                abort(404, description=f'Unknown status {status}')
            found_users.append((user.username, buttons))
    return render_template("add-friend.html", search_form=search_form, found_users=found_users)


@myapp_obj.route("/add-friend/<int:user_id>", methods=['GET', 'POST'])
@login_required
def add_friend_userid_provided(user_id):
    # Abort if adding self as friend
    if int(current_user.get_id()) == user_id:
        return abort(404, description="Cannot add yourself as friend")
    status, friend_record = get_friend_status(current_user.get_id(), user_id)
    if status == 'friend':
        # Already a friend, do nothing
        pass
    elif status == 'pending-sent-request':
        # Current user sent a request, do nothing
        flash(f'Friend request already sent to "{friend_record.user2.username}"')
    elif status == 'pending-to-approve':
        # Other user sent the request, approve (Change status from pending to approved)
        friend_record.status = FriendStatusEnum.FRIEND
        db.session.add(friend_record)
        db.session.commit()
        flash(f'Approved friend request from "{friend_record.user1.username}"')
    elif status == 'neutral':
        # No friendship record found, send friend request
        user = User.query.filter_by(id=user_id).one()
        friend = Friend(user1_id=current_user.get_id(), user2_id=user.id, status=FriendStatusEnum.PENDING)
        db.session.add(friend)
        db.session.commit()
        flash(f'Sent friend request to "{user.username}"')
    else:
        abort(404, description=f"Unknown status {status}")
    return redirect(url_for("show_friends"))


@myapp_obj.route("/remove-friend/<int:user_id>", methods=['GET', 'POST'])
@login_required
def remove_friend_userid_provided(user_id):
    # Abort if removing self as friend
    if int(current_user.get_id()) == user_id:
        return abort(404, description="Cannot remove yourself from friend")
    status, friend_record = get_friend_status(current_user.get_id(), user_id)
    if friend_record:
        other_user = friend_record.user1.username if friend_record.user1.id != int(current_user.get_id()) else friend_record.user2.username
        if status == 'friend':
            flash(f'Removed "{other_user}" from friend')
        elif status == 'pending-sent-request':
            flash(f'Unsent friend request to "{other_user}"')
        elif status == 'pending-to-approve':
            flash(f'Rejected friend request from "{other_user}"')
        elif status == 'neutral':
            pass # Do nothing
        else:
            abort(404, description=f'Unknown status {status}')
        db.session.delete(friend_record)
        db.session.commit()
    return redirect(url_for("show_friends"))


#Pomodoro app
@myapp_obj.route("/pomodoro")
def tomato():
    return render_template("/pomodoro.html")


@myapp_obj.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404

myapp_obj.register_error_handler(404, page_not_found)
