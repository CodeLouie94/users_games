from flask_app import app, bcrypt
from flask import render_template, redirect, session, request

from flask_app.models import model_user

@app.route('/logout')
def logout():
    del session['uuid']
    return redirect('/')

@app.route('/user/new')
def user_new():
    return render_template('user_new.html')

@app.route('/user/process_login', methods=['POST'])
def process_login():
    if not model_user.User.validate_login(request.form):
        return redirect('/')
    return redirect('/')

@app.route('/user/create', methods=['POST'])
def user_create():
    if not model_user.User.validate_registration(request.form):
        return redirect('/user/new')
    
    hash_pw = bcrypt.generate_password_hash(request.form['pw'])
    data= {
        **request.form,
        'pw': hash_pw
    }

    id = model_user.User.create(data)
    session['uuid'] = id
    return redirect('/')

@app.route('/user/<int:id>')
def user_show():
    return render_template('user_show.html')

@app.route('/user/<int:id>/edit')
def user_edit():
    return render_template('user_edit.html')

@app.route('/user/<int:id>/update', methods =['POST'])
def user_update():
    return redirect('/')


@app.route('/user/<int:id>/delete')
def user_delete():
    return redirect('/')