from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, Email, Optional, URL

from bluelog import Category


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(1,20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(1,20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(1,50)])
    category = StringField('Category', coerce=int,default=1)
    body = CKEditorField('Body',validators=[DataRequired()])
    submit = SubmitField()
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]
class Category(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(1,20)])
    submit = SubmitField()
    def validate_name(self,field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')

class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(),Length(1,30)])
    email = StringField('Email',validators=[DataRequired(),Email(),Length(1,30)])
    site = StringField('Site',validators=[Optional(),URL(),Length(0,255)])
    body = TextAreaField('Comment',validators=[DataRequired()])
    submit =  SubmitField()

class AdminComment(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site =  HiddenField()
