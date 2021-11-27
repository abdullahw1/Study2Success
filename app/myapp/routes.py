from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify, abort
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required

from myapp import myapp_obj, db, nav
from myapp.forms import SignupForm, LoginForm, FlashCardForm, UploadMarkdownForm, SearchForm, ShareFlashCardForm
from myapp.models import User, FlashCard, Friend, FriendStatusEnum, Todo, SharedFlashCard
from myapp.models_methods import get_friend_status, get_all_friends
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

# Flashcards
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


@myapp_obj.route("/my-flashcards")
@login_required
def show_flashcard():
    # cards = FlashCard.query.filter_by(user_id = current_user.get_id()).all()
    ordered_cards = FlashCard.query.filter_by(user_id=current_user.get_id()).order_by(FlashCard.learned).all()
    if ordered_cards is None:
        flash("You don't have any flashcards. Please create one")
        return redirect(url_for("add_flashcard"))
    return render_template("my-flashcards.html", ordered_cards=ordered_cards)


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


@myapp_obj.route("/learn-flashcard", methods=['GET', 'POST'])
@login_required
def learn_flashcard():
    # Not implemented yet, redirect back
    flash(f'Feature not implemented yet')
    return redirect(url_for("show_flashcard"))


@myapp_obj.route("/remove-flashcard/<int:flashcard_id>", methods=['GET', 'POST'])
@login_required
def remove_flashcard(flashcard_id):
    flashcard = FlashCard.query.filter_by(id=flashcard_id).one_or_none()
    if flashcard:
        flash(f'Deleted flashcard front="{flashcard.front}", back="{flashcard.back}"')
        db.session.delete(flashcard)
        db.session.commit()
    return redirect(url_for("show_flashcard"))


@myapp_obj.route("/share-flashcard/<int:flashcard_id>", methods=['GET', 'POST'])
@login_required
def share_flashcard(flashcard_id):
    flashcard = FlashCard.query.filter_by(id=flashcard_id).one_or_none()
    if not flashcard:
        abort(404, Description=f'Unable to find flashcard with id {flashcard_id}')
    friends = []
    for status, oth_user in get_all_friends(current_user.get_id()):
        if status == 'friend': # Only find friends
            friends.append(oth_user)
    form = ShareFlashCardForm()
    form.dropdown.choices = [(u.id, u.username) for u in friends]
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.dropdown.data).one()
        now = datetime.now()
        share_card = SharedFlashCard(flashcard_id=flashcard_id,
                                    datetime=now,
                                    owner_user_id=current_user.get_id(),
                                    target_user_id=user.id)
        db.session.add(share_card)
        db.session.commit()
        flash(f'Shared flashcard(#{flashcard_id}) to "{user.username}" on {str(now)}')
        return redirect(url_for("show_flashcard"))
    return render_template("share-flashcard.html", flashcard=flashcard, form=form)


@myapp_obj.route("/flashcards-sharing", methods=['GET', 'POST'])
@login_required
def flashcards_sharing():
    owner_flashcards = SharedFlashCard.query.filter_by(owner_user_id=current_user.get_id()).all()
    target_flashcards = SharedFlashCard.query.filter_by(target_user_id=current_user.get_id()).all()
    return render_template("flashcards-sharing.html", owner_flashcards=owner_flashcards, target_flashcards=target_flashcards)


@myapp_obj.route("/flashcards-sharing/add-to-myflashcards/<int:sharing_id>", methods=['GET', 'POST'])
@login_required
def flashcards_sharing_add_to_myflashcards(sharing_id):
    sharing = SharedFlashCard.query.get(sharing_id)
    if int(current_user.get_id()) != sharing.owner_user_id and\
        int(current_user.get_id()) != sharing.target_user_id:
        abort(404, description='Invalid permission')
    card = FlashCard(front=sharing.flashcard.front, back=sharing.flashcard.back, learned=0, user=current_user._get_current_object())
    db.session.add(card)
    db.session.commit()
    flash(f'Copied flashcard(#{sharing.flashcard.id}) to "My Flashcards", new flashcard(#{card.id})')
    return redirect(url_for('flashcards_sharing'))


@myapp_obj.route("/flashcards-sharing/cancel-sharing/<int:sharing_id>", methods=['GET', 'POST'])
@login_required
def flashcards_sharing_cancel_sharing(sharing_id):
    sharing = SharedFlashCard.query.get(sharing_id)
    if int(current_user.get_id()) != sharing.owner_user_id and\
        int(current_user.get_id()) != sharing.target_user_id:
        abort(404, description='Invalid permission')
    flash(f'Sharing of flashcard(#{sharing.flashcard.id}) cancelled')
    db.session.delete(sharing)
    db.session.commit()
    return redirect(url_for('flashcards_sharing'))



# Friends
@myapp_obj.route("/my-friends", methods=['GET', 'POST'])
@login_required
def show_friends():
    # Handle show all friends
    friends = []
    for status, oth_user in get_all_friends(current_user.get_id()):
        if status == 'friend':
            buttons = [(f'/remove-friend/{oth_user.id}', 'Remove Friend')]
            print_status = 'Friend'
        elif status == 'pending-sent-request':
            buttons = [(f'/remove-friend/{oth_user.id}', 'Unsend')]
            print_status = 'Sent'
        elif status == 'pending-to-approve':
            buttons = [(f'/add-friend/{oth_user.id}', 'Approve'), (f'/remove-friend/{oth_user.id}', 'Reject')]
            print_status = 'Pending'
        else:
            abort(404, f'Unknown status {status}')
        friends.append((oth_user, print_status, buttons))
    # Handle Add user
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
    return render_template("my-friends.html", friends=friends, search_form=search_form, found_users=found_users)


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

# Todo app
@myapp_obj.route("/todo")
def myTodo():
    todo_list = Todo.query.all()
    return render_template("todo.html", todo_list=todo_list)

@myapp_obj.route("/addTodo", methods=["POST"])
def addTodo():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("myTodo"))

@myapp_obj.route("/updateTodo/<int:todo_id>")
def updateTodo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("myTodo"))

@myapp_obj.route("/deleteTodo/<int:todo_id>")
def deleteTodo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("myTodo"))

@myapp_obj.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404

myapp_obj.register_error_handler(404, page_not_found)
