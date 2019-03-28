from flask import Blueprint
from flask import redirect, url_for, render_template, redirect, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app import db, bcrypt
from app.models.user import User
from app.models.post import Post
from app.users.forms import RegistrationForm, LoginForm, UpdateUserInfoForm
from app.users.forms import RequestPasswordResetForm, PasswordResetForm
from app.users.utils import save_new_user_pic, delete_old_pic, send_reset_email

users = Blueprint('users', __name__)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user already logged in redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_psw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_psw)

        db.session.add(user)
        db.session.commit()

        flash(f'Account successfully created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('signup.html', title='Sign Up', form=form)


@users.route('/login', methods=['GET','POST'])
def login():
    # If user already logged in redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Finds and returns the user with the specified email address
            user = User.query.filter_by(email=form.email.data.lower()).first()

            # Verbose error messages vulnerability
            if user is None:
               flash(f'Failed login. No account exists with the provided email address', 'danger')

            elif user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                session['_id'] = '123abc' # weak session ids !
                next_page = request.args.get('next') # get next value from url query string
                if next_page:
                    return redirect(url_for(next))
                else:
                    return redirect(url_for('main.home'))
            else:
                # Verbose error messages vulnerability
                flash(f'Failed login. Password invalid', 'danger')


    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateUserInfoForm()
    if form.validate_on_submit():
        if form.picture.data:
            new_pic_fname = save_new_user_pic(form.picture.data)
            delete_old_pic(current_user.image_file) # delete old user image
            current_user.image_file = new_pic_fname # update user data
        if form.email.data:
            current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash('Account info has been updated succesfully', 'success')
        return redirect(url_for('users.profile'))

    elif request.method == 'GET':
        # populating form fields with current user info
        form.username.data = current_user.username
        form.email.data = '' #current_user.email  # empty for UI redress attack



    avatar = url_for('static', filename='assets/users/' + current_user.image_file)


    return render_template('profile.html', title='User Profile', user_avatar=avatar,
                            form=form)


@users.route('/user/<string:username>')
def user_posts(username):
    #Returns the posts from submitted by a specific user
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user)\
                      .order_by(Post.date_posted.desc())\
                      .paginate(page=page, per_page=5)

    return render_template('posts/user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestPasswordResetForm()

    if request.method == 'GET':
        return render_template('req_password_reset.html', title='Reset Password', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_reset_email(user)
            # The user gets the same message displayed, even if no user exist with the provided email
            # This reduces the info given to an attacker trying to enumerate existing accounts
            flash('An email with the instructions has been sent to the specified email address', 'success')
            return redirect(url_for('main.home'))


@users.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_psw_reset_token(token)
    form = PasswordResetForm()
    if request.method == 'GET':
        if not user:
            flash('Invalid or expired link', 'warning')
            return redirect(url_for('main.home'))
        else:
            return render_template('reset_password.html', title='Reset password', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            hashed_psw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_psw
            db.session.commit()
            flash(f'Your password has been succesfully reset. Please login again', 'success')
            return redirect(url_for('users.login'))
        else:
            flash('An error has occured. The password has NOT been reset. Please contact the admin...', 'warning')
            return redirect(url_for('main.home'))
