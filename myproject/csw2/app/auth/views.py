from flask import render_template, flash, redirect, url_for,Flask
from flask_login import login_user, logout_user, login_required, current_user
from flask.globals import request
from .. import db
from . import auth
from .forms import SignupForm, LoginForm
from ..models import User
from sqlalchemy import exc

@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            user = User(email       =form.email.data,
                        username    =form.username.data,
                        password    =form.password.data)
            try:    
                db.session.add(user)
                db.session.commit()
                flash('Registeration complete. please login.')                
                return redirect(url_for('auth.login'))
            except exc.IntegrityError:
                db.session.rollback()
                flash('This e-mail in use already.')
        else:
            flash('Already registed user.')        
    return render_template('auth/signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        
        # check if the user actually exists 
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
            
        flash('Double check your email or password')   
    return render_template('auth/login.html', form=form)

# @auth.route("/user")
# def user():
#     if "user" in session:
#         user = session["user"]
#         return f"<h1>{user}</h1>"
#     else:
#         return redirect(url_for("auth.login"))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sign out completed...')
    return redirect(url_for('main.index'))  

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()