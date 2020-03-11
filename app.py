#Libraries

import os
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, RadioField, validators
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Configuration

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo_secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Migrate(app, db)

#Database Models
class User(db.Model):
    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    sex = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)
    def __init__(self, name, sex, email, password):
        self.name = name
        self.sex = sex
        self.email = email
        self.password = password

class Category(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.Text, unique=True, nullable=False)

class Videos(db.Model):
    v_id = db.Column(db.Integer, primary_key=True)
    v_name = db.Column(db.Text, nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.c_id'), nullable=False)

#Forms

class RegistrationForm(FlaskForm):
    name = StringField("NAME", [
        validators.DataRequired()
    ])
    email = StringField("EMAIL", [
        validators.Email()
    ])
    sex = RadioField("ARE YOU MALE OR FEMALE?", [
        validators.DataRequired(),
    ],
    choices=[("sex_one", "MALE"), ("sex_two", "FEMALE")])
    password = PasswordField("PASSWORD", [
        validators.DataRequired(),
        validators.Length(min=10),
        validators.EqualTo("confirm_password", message="PASSWORDS MUST MATCH!")])
    confirm_password = PasswordField("CONFIRM PASSWORD")
    if password == confirm_password:
        flash("PASSWORDS MATCHED.")
    t_and_c = BooleanField("I AGREE TO THE TERMS AND CONDITIONS.", [
        validators.DataRequired(),
    ])
    submit = SubmitField("SIGN UP")

class LoginForm(FlaskForm):

#Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/registration', methods = ["GET", "POST"])
def register():
    registrationform = RegistrationForm(request.form)
    if request.method == 'POST' and registrationform.validate():
        sex_value = ""
        session["name"] = registrationform.name.data
        session["sex"] = registrationform.sex.data
        if session["sex"] == "sex_one":
            sex_value = "MALE"
        elif session["sex"] == "sex_two":
            sex_value = "FEMALE"
        session["email"] = registrationform.email.data
        session["password"] = registrationform.password.data
        new_record = User(name=session["name"], sex=sex_value, email=session["email"], password=session["password"])
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('registrationsuccessful'))
    return render_template('register.html', form = registrationform)

@app.route('/user/registration/registrationsuccessful')
def registrationsuccessful():
    return render_template('registration_successful.html')

@app.route('/user/login')
def login():
    return render_template('login.html')

@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories = categories)

@app.route('/categories/<category_videos>')
def category_videos(category_videos):
    return render_template('category_videos.html', category_videos = category_videos)

if __name__ == '__main__':
    app.run()
