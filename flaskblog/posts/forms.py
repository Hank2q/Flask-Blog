from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Post Title', validators=(
        [DataRequired(), Length(min=1, max=250)]))

    content = TextAreaField('Post Content', validators=([DataRequired()]))
    submit = SubmitField('Post')
