from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.form.get("login"):
        userName = request.form.get('userName')
        password = request.form.get('password')
        username = User.query.filter_by(userName=userName).first()
        
        if username:
            if check_password_hash(userName.password, password):
                login_user(userName, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Account does not exist', category='error')
    
    elif request.form.get("register"):
        userName = request.form.get('userName')
        password = request.form.get('password')
        
        username = User.query.filter_by(userName=userName).first()
        if username:
            flash('User Name already exist.', category='error')
        elif len(userName) < 4:
            flash('Invalid Email', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(userName=userName, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)                
            return redirect(url_for('views.home'))
        
    return render_template("login.html", user=current_user )


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))