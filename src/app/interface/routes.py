from flask import render_template, request, redirect, url_for
from app.interface import app
from .models import User
from .main import db


@app.route('/')
def index():
    incomplete = User.query.filter_by(complete=False).all()
    complete = User.query.filter_by(complete=True).all()

    return render_template('index.html', incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    User = User(text=request.form['Useritem'], complete=False)
    db.session.add(User)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):

    User = User.query.filter_by(id=int(id)).first()
    User.complete = True
    db.session.commit()

    return redirect(url_for('index'))
