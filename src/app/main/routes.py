from flask import Flask, render_template, request, current_app, redirect, url_for, session
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from ..chatbot.bot import get_completion
from ..models import db
from ..models.user_model import Users


@current_app.route("/")
@login_required
def home():
    return render_template("index.html", current_user=current_user)


@current_app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = get_completion(userText)
    return response

@current_app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@current_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@current_app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if user already exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('register.html', error="Username already exists")
        
        # Create new user
        new_user = Users(
            username=username,
            password=generate_password_hash(password, method='scrypt')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')