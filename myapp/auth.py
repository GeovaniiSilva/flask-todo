from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import login_user

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('auth/login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Email or password is incorrect!')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('main.home'))


@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if password != password2:
        flash('Passwords are not equal!')
        return redirect(url_for('auth.signup'))
    
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email already in use!')
        return redirect(url_for('auth.signup'))

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='sha256')
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    return 'Logout'

