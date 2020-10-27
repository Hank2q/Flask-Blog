from os.path import splitext as get_ext, join
from PIL import Image
from flask_mail import Message
from flaskblog import app, mail
from flask import url_for


def update_profile_img(form_img, user_name):
    _, ext = get_ext(form_img.filename)
    pic_name = user_name + ext
    pic_path = join(app.root_path, 'static/images/profiles', pic_name)
    i = Image.open(form_img)
    i.thumbnail((150, 150))
    i.save(pic_path)
    return pic_name


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password reset',
                      sender='noreply@polarblog.com', recipients=[user.email])
    message.body = f'''\
To reset your password follow the link bellow:
{url_for('users.reset_password', token=token, _external=True)}'''
    mail.send(message)
