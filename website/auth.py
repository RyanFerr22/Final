from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login', methods = ['GET','POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            flash('logged in successfully', category='success')
            login_user(user,remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('incorrect password', category='error')
    
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        access_lvl = int(request.form.get('access_lvl'))
        
        user = User.query.filter_by(email=email).first()
        userName = User.query.filter_by(username=username).first()
        
        if user:
            flash('Email already exists', category='error')
        if userName:
            flash('Username already exists', category='error')
        elif len(username) < 3:
            flash("Username must be greater than two characters", category= 'error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category = 'error')
        elif password1 != password2:
            flash("Passwords don\' match", category = 'error')
        elif len(password1) < 7:
            flash("Passwords must be at least 7 characters", category = 'error')
            
        else:
            new_user = User(username=username,email=email,password=(generate_password_hash(password1,method='pbkdf2:sha256')),access_lvl = access_lvl)
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created!", category="success")
            return redirect(url_for('auth.login'))
        
    return render_template("sign_up.html", user=current_user)

@auth.route('/admin_signup', methods = ['GET','POST'])
@login_required
def admin_signup():
    if request.method == 'POST':
        password = request.form.get('password')
        
        a_s_ep_password = "FinalOOP2Project.EP^&"
        a_s_a_password = "FinalOOP2Project.ADMIN&^"
        
        if password == a_s_ep_password:
            found_user = User.query.filter_by(id=current_user.id).first()
            found_user.access_lvl = 1
            db.session.commit()
            print(current_user.access_lvl)
            flash("You are now an Official Event Planner!", category='success')
            return redirect(url_for('views.home'))
        
        if password == a_s_a_password:
            found_user = User.query.filter_by(id=current_user.id).first()
            found_user.access_lvl = 2
            db.session.commit()
            print(current_user.access_lvl)
            flash("You are now an Official Admin!", category='success')
            return redirect(url_for('views.home'))
            
    return render_template("admin_signup.html", user=current_user)
    