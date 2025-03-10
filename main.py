"""from flask import Flask, abort, render_template, redirect, url_for, flash, request,session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import Integer, String, Float,ForeignKey
from flask_bootstrap import Bootstrap5
from forms import contactForm, registerForm, loginForm, addForm
from email_class import mail
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_wtf.csrf import CSRFProtect
import stripe
from dotenv import load_dotenv
import os"""