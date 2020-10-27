from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.model import User
from flask_login import current_user
from flaskblog import bcrypt


class RegestrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Regester')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken, try another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use, try another email')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_img = FileField('Update Profile Picture',
                            validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    update = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username taken, try another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'Email already in use, try another email')


class PostForm(FlaskForm):
    title = StringField('Post Title', validators=(
        [DataRequired(), Length(min=1, max=250)]))

    content = TextAreaField('Post Content', validators=([DataRequired()]))
    submit = SubmitField('Post')


class RequerstResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    request = SubmitField('Requerst Password Reset')

    # ! revelaing that an email is not associated with an accout is a security flaw
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is None:
    #         raise ValidationError('There is no account with this email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
                             DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField(
        'Confirm New Password', validators=[DataRequired(), EqualTo('password')])

    reset = SubmitField('Reset Password')


class ChangePassword(FlaskForm):
    old_password = PasswordField('Old Password', validators=[
        DataRequired(), Length(min=6, max=20)])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), Length(min=6, max=20)])
    confirm_new_password = PasswordField(
        'Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])

    change = SubmitField('Change Password')

    def validate_old_password(self, old_password):
        if not bcrypt.check_password_hash(current_user.password, old_password.data):
            raise ValidationError('Old password does not match, Try again.')

    def validate_new_password(self, new_password):
        if bcrypt.check_password_hash(current_user.password, new_password.data):
            raise ValidationError(
                'New and Old passwords cannot be the same. Chose a different password')
