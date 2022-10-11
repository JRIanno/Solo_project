from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.coffee import Roasts
from flask_app.models.users import Users

@app.route('/roasts')
def roasts():
    if 'user_id' not in session:
        return redirect('/register')
    data = {
        'id': session['user_id'],
    }
    print(data)
    return render_template('roasts.html', users=Users.get_id(data), roasts=Roasts.get_all())

@app.route('/new/roasts')
def new_roast():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id'],
    }
    return render_template('question.html', users=Users.get_id(data))

@app.route('/new/roast/new', methods=['POST'])
def add_2_roast():
    if not Roasts.validate_roastname(request.form):
        return redirect('/new/roasts')

    data = {
        'user_id': request.form['user_id'],
        'name': request.form['name'],
        'origin': request.form['origin'],
        'start_temp': request.form['start_temp'],
        'start_time': request.form['start_time'],
        'degree': request.form['degree'],
        'first_time': request.form['first_time'],
        'first_temp': request.form['first_temp'],
        'level': request.form['level'],
        'time': request.form['time'],
        'share': request.form['share'],
    }
    if 'user_id' not in session:
        return redirect('/')
    
    Roasts.submit(data)
    return redirect('/roasts')

@app.route('/profile/<int:id>')
def profile(id):
    
    data = {
        'id': id,
        'id': session['user_id'],
    }
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('profile.html', users=Users.get_all_by_id(data))


@app.route('/one/roast/<int:roast_id>')
def single_roast(roast_id):
    data = {
        'id': id,
        'id': session['user_id'],
    }
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('individual.html',users = Users.get_id(data), roasts=Roasts.one_roast(roast_id))


@app.route('/roast/<int:roast_id>/edit')
def edit_roast(roast_id):
    return render_template('edit.html', roasts = Roasts.one_roast(roast_id))

@app.route('/edit/<int:roast_id>', methods=['POST'])
def roast_edit(roast_id):
    data = {
        'id': request.form['id'],
        'user_id': request.form['user_id'],
        'degree': request.form['degree'],
        'first_time': request.form['first_time'],
        'first_temp': request.form['first_temp'],
        'level': request.form['level'],
        'time': request.form['time'],
        'share': request.form['share'],
    }
    if 'user_id' not in session:
        return redirect('/')
    Roasts.update_roast(data)
    return redirect(f'/one/roast/{roast_id}')

@app.route('/delete/<int:roast_id>')
def delete(roast_id):
    Roasts.delete(roast_id)
    return redirect('/roasts')