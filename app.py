from flask import Flask, render_template, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from forms import RegestrationForm, LoginForm
app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = '71d0d5d303a191c0d1ec20f3d03dd6f6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(210), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    profile_img = db.Column(
        db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship("Post", backref='author', lazy=True)

    def __repr__(self):
        return f'{type(self).__name__}({self.username}, {self.email}, {self.profile_img})'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    post_date = db.Column(db.DateTime, nullable=False,
                          default=datetime.datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{type(self).__name__}({self.title}, {self.post_date})'
# * to have multiple url paths leading to the same page, use multiple decorators


@app.route('/')
@app.route('/home')
def home():
    # ! no need to specify parent dir if its named templates, else have to mention i.e. pages/home.html
    return render_template('home.html', posts=posts, style='home')


@app.route('/about')
def about():
    return render_template('about.html', style='about')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/regester', methods=['GET', 'POST'])
def regester():
    form = RegestrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('regester.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


# * use this to run the script directly instead of > flask run
if __name__ == "__main__":
    app.run(debug=True)
