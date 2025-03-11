from flask import Flask, abort, render_template, redirect, url_for, flash, request,session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import Integer, String, Float,ForeignKey,Boolean
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

Bootstrap(app)
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


if __name__ == "__main__":
    app.run(debug=True,port=5000)