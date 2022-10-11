from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.users import Users
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    
    return render_template('home.html')

@app.route('/register')
def register():

    return render_template('register.html')

@app.route('/register/user', methods=['POST'])
def reg_post():
    if not Users.valid_register(request.form):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = Users.save(data)
    session['user_id'] = user_id
    return redirect('/roasts')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/valid', methods=['POST'])
def log_val():
    data = {'email': request.form['email']}
    db_user = Users.valid_login(data)
    if not db_user:
        flash("I'm sorry, but it seems as though your email and or password are incorrect.")
        return redirect('/login')
    if not bcrypt.check_password_hash(db_user.password, request.form['password']):
        flash("I'm sorry, but it seems as though your email and or password are incorrect.")
        return redirect('/login')
    session['user_id'] = db_user.id
    return redirect('/roasts')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')