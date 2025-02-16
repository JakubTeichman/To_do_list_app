from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from models import User
from forms import LoginForm, RegisterForm

user_mg = Blueprint('user_mg', __name__)
login_manager = LoginManager() 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@user_mg.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.role == 'admin':
                return redirect(url_for('task_mg.admin_view'))
            return redirect(url_for('task_mg.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@user_mg.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2')
        new_user = User(username=form.username.data, email=form.email.data ,password=hashed_password, role = form.role.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user_mg.login'))
    flash('Invalid username or email')
    return render_template('register.html', form=form)

@user_mg.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_mg.login'))   
