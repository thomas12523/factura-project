from flask import Flask, abort, render_template, redirect, url_for, flash, request,session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import Integer, String,ForeignKey,Boolean
from flask_bootstrap5 import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
#from flask_wtf.csrf import CSRFProtect
from forms import loginForm,registerForm
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
ckeditor = CKEditor(app)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facturas.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# DB Tables

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)

    # Relación con facturas (un usuario puede tener muchas facturas)
    facturas = relationship("Facturas", back_populates="user", cascade="all, delete-orphan")

class Facturas(db.Model):
    __tablename__ = "facturas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_vto: Mapped[str] = mapped_column(String(1000), nullable=False)
    monto_total: Mapped[int] = mapped_column(Integer, nullable=False)
    pagado: Mapped[bool] = mapped_column(Boolean, default=False)

    # Foreing Key
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # Relación inversa con User
    user = relationship("User", back_populates="facturas")


with app.app_context():
    db.create_all()  


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = loginForm()
    if form_login.validate_on_submit():
        email = form_login.email.data
        password = form_login.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not user:
            flash('Email doesn\'t exist, please try again.')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form_login, current_user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = registerForm()
    if register_form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == register_form.email.data)).scalar()
        if not user:
            hash_and_salted = generate_password_hash(register_form.password.data, method="pbkdf2:sha256", salt_length=8)
            new_user = User(email=register_form.email.data, name=register_form.username.data, password=hash_and_salted)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
        else:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
    return render_template('register.html', form=register_form)

if __name__ == "__main__":
    app.run(debug=True,port=5000)