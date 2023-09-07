from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class CreateProductForm(FlaskForm):
    title = StringField("Product Title", validators=[DataRequired()])
    subtitle = StringField("Product Description", validators=[DataRequired()])
    img_url = StringField("Product Image URL", validators=[DataRequired(), URL()])
    product_url = StringField("Product Purchase URL", validators=[DataRequired(), URL()])
    price = StringField("Product Price", validators=[DataRequired()])
    # body = CKEditorField("Product Description", validators=[DataRequired()])
    submit = SubmitField("Submit Product")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit Post")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class CommentForm(FlaskForm):
    comment = CKEditorField("Comments", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")