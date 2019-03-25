from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    post_img = FileField('Post image', validators=[FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Content', validators=[DataRequired()])

    submit = SubmitField('Submit')
