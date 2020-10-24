from flask import render_template, flash, url_for, redirect, request, abort, jsonify
from flaskblog import app, bcrypt, db
from flaskblog.forms import RegestrationForm, LoginForm, UpdateForm, PostForm
from flaskblog.model import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from os.path import splitext as get_ext, join
from PIL import Image
# * to have multiple url paths leading to the same page, use multiple decorators

# ? the first arg in url_for is the name of the function u gave and then
# ? the arguments u specified if any


@app.route('/')
@app.route('/home')
def home():
    # ! no need to specify parent dir if its named templates, else have to mention i.e. pages/home.html
    posts = Post.query.all()
    posts.reverse()
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/regester', methods=['GET', 'POST'])
def regester():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
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
        return redirect(url_for('login'))
    return render_template('regester.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful, Please check email and password', 'error')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def update_profile_img(form_img, user_name):
    _, ext = get_ext(form_img.filename)
    pic_name = user_name + ext
    pic_path = join(app.root_path, 'static/images/profiles', pic_name)
    i = Image.open(form_img)
    i.thumbnail((150, 150))
    i.save(pic_path)
    return pic_name


@app.route('/account', methods=['GET', 'POST'])
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
        redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.submit()
    image = url_for('static', filename='images/profiles/' +
                    current_user.profile_img)
    posts = current_user.posts
    posts.reverse()
    return render_template('account.html', image=image, form=form, posts=posts)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created', 'success')
        return redirect(url_for('home'))
    return render_template('newPost.html', form=form, legend="New Post")


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    posts = user.posts
    posts.reverse()
    return render_template('user.html', user=user, posts=posts)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated', 'success')
        return redirect(url_for('post', post_id=post_id))
    elif request.method == "GET":
        form.submit.label.text = "Update"
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newPost.html', form=form, legend="Update Post")


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post: "{post.title}" Deleted', 'info')
    page = request.args.get('page')
    if page:
        return redirect(url_for(page))
    return redirect(url_for('home'))


@app.route('/data')
def data():
    posts = Post.query.all()
    json = [{'id': p.id, 'title': p.title,
             'authour': p.author.username, 'date': p.post_date} for p in posts]
    return jsonify(json)
