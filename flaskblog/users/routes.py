from flask import Blueprint
from flask import render_template, flash, url_for, redirect, request
from flaskblog import bcrypt, db, POSTS_PER_PAGE
from flaskblog.users.forms import RegestrationForm, LoginForm, UpdateForm, RequerstResetForm, ResetPasswordForm, ChangePassword
from flaskblog.model import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import send_reset_email, update_profile_img

users = Blueprint('users', __name__)


@users.route('/regester', methods=['GET', 'POST'])
def regester():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = RegestrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Account created for {form.username.data}, You can login now!', 'success')
        return redirect(url_for('users.login'))
    return render_template('regester.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful, Please check email and password', 'error')
    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.profile_img.data:
            picture_file = update_profile_img(
                form.profile_img.data, form.username.data)
            current_user.profile_img = picture_file
            db.session.commit()
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account information updated', 'info')
        redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static', filename='images/profiles/' +
                    current_user.profile_img)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=current_user).order_by(
        Post.post_date.desc()).paginate(per_page=POSTS_PER_PAGE, page=page)
    return render_template('account.html', image=image, form=form, posts=posts)


@users.route('/user/<string:username>')
def user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user).order_by(
        Post.post_date.desc()).paginate(per_page=POSTS_PER_PAGE, page=page)
    return render_template('user.html', user=user, posts=posts)


@users.route('/reset/request', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = RequerstResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('If an account with this email address exists, a password reset message will be sent shortly', 'info')
        return redirect(url_for('main.home'))
    return render_template('requestReset.html', form=form)


@users.route('/reset/password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or Expired Token, Try Again.', 'error')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(
            f'Password updated', 'success')
        return redirect(url_for('users.login'))
    return render_template('passwordReset.html', form=form)


@users.route('/reset', methods=['GET', 'POST'])
@users.route('/reset/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.new_password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash(
            f'Password Changed', 'success')
        return redirect(url_for('users.account'))
    return render_template('changePassword.html', form=form)
