from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, EmailField,FileField,SelectField,PasswordField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class registerForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    email=EmailField("Email",validators=[DataRequired()])
    password=StringField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")

class loginForm(FlaskForm):
    email=EmailField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")

class addFactura(FlaskForm):
    proveedor = SelectField("Proveedor", choices=[
        ("metrogas", "Metrogas"),
        ("movistar", "Movistar"),
        ("edenor","Edenor"),
        ("edesur","Edesur")
    ], validators=[DataRequired()])
    email=StringField("Product Name",validators=[DataRequired()])
    archivo=FileField('Subir PDF', validators=[DataRequired(), FileAllowed(['pdf'], 'Solo se permiten archivos PDF.')])
    submit = SubmitField("Submit")