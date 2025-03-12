from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, EmailField,IntegerField,SelectField,PasswordField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired


class registerForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    email=EmailField("Email",validators=[DataRequired()])
    password=StringField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")

class loginForm(FlaskForm):
    email=EmailField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")

class addForm(FlaskForm):
    category = SelectField("Category", choices=[
        ("rat-poison", "Rat Poison"),
        ("Cockroaches", "Cockroaches")
    ], validators=[DataRequired()])
    price=IntegerField("Price",validators=[DataRequired()])
    name=StringField("Product Name",validators=[DataRequired()])
    img=StringField("Name of Image",validators=[DataRequired()])
    description=CKEditorField("Product's Description", validators=[DataRequired()])
    submit = SubmitField("Submit")