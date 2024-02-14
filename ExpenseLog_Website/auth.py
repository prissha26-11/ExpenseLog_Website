from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required,logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, ValidationError

auth = Blueprint('auth',__name__)

    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max= 15, message="Username should be between 4 to 15 characters.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=80)])
    remember = BooleanField('Remember me')

    def validate_password(form, field):
        username_entered = form.username.data
        user = User.query.filter_by(username=username_entered).first()
        if user:
            if not check_password_hash(user.password,field.data):
                raise ValidationError('Incorrect Password')
    
    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError('Username does not exist.')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max= 15)])
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max= 15)])
    password1 = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=80)])
    password2 = PasswordField('ReEnter Password', validators=[InputRequired()])

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Username already exist.')
    
    def validate_password2(form, field):
        password1 = form.password1.data
        if password1 != field.data:
            raise ValidationError('Passwords do not match.')


@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!', category='success')
                login_user(user,remember=remember)

                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password,try again',category='error')

        else:
            flash('Username does not exist.',category='error')

    return render_template("login.html",user=current_user, form =form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up',methods=['GET','POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        username = form.username.data
        name = form.name.data
        password1 = form.password1.data
        password2 = form.password2.data

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Email already exist.',category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        else:
            new_user =User(username=username,first_name=name,password=generate_password_hash(password1,method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
            # add user to database
    return render_template("sign_up.html",user=current_user, form =form)