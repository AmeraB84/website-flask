import email
from flask import Blueprint, render_template, request, flash,redirect,url_for
from website.models import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        #get user 
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password,password):
                flash('Logged is successfully ! ', category='success')

                #Faire en sortie que le browser se souviens dun user si il s'est déja connecté 
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password , try again .',category='error')
        else:
            flash('Email does not exist !! ', category='error')

    return render_template("login.html" ,user = current_user)




@auth.route('/logout')
@login_required
def logout():
    # s'assurer que user est déja loguée 
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sighup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #get user 
        user = User.query.filter_by(email=email).first()
        
        #check if user exist 
        if user : 
            flash('Email already exist !!',category='error')

        # If not exist validate form and add user to db 
        elif len(email) < 4:
            flash('Email must be greater than 4 characters ', category='error')
        elif len(firstname) < 2:
            flash('FirstName must be greater then 2 characters ! ', category='error')
        elif password1 != password2:
            flash('both passwords must be eqal ! ',category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters ! ',category='error')
        else:
            # add user to database
            new_user = User(email=email,first_name=firstname,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            #Faire en sortie que le browser se souviens dun user si il s'est déja connecté 
            login_user(new_user,remember=True)

            flash('Account created !! ', category='success')
            return redirect(url_for('views.home'))
    return render_template('sign-up.html',user=current_user)
