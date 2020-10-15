from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
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
                          default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{type(self).__name__}({self.title}, {self.post_date})'
