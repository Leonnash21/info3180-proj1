"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for, Flask, flash, jsonify
from flask.ext.wtf import Form
from wtforms.fields import TextField, FileField, SelectField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import Required
from flask_wtf.file import FileField, FileAllowed, FileRequired
import os
import math
from app import db
from app.models import User
from werkzeug import secure_filename
from datetime import date, datetime
from time import strftime 
import random
from random import randrange, randint



class ProfileForm(Form):
    username = TextField('Username', validators=[Required()])
    firstname = TextField('Firstname', validators=[Required()])
    lastname = TextField('Lastname', validators=[Required()])
    age = IntegerField('Age', validators=[Required()])
    sex = SelectField('Sex', choices=[('Male', 'Male'), ('Female','Female')], validators=[Required()])
    image = FileField('Profile Photo', validators=[FileRequired(), FileAllowed(['jpg,png'], 'Images Only!')])
    


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
    
@app.route('/profile/', methods = ['GET', 'POST'])
def add_profile():
    form = ProfileForm()
    
    if request.method == 'POST':
        # if form.validate_on_submit():
            username = request.form ['username']
            # userid = str(random.randrange(1000000, 1099999,[1]))
            userid = random.randint(1000000, 1099999)
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            age = request.form['age']
            sex =  request.form['sex']
           
            file = request.files['image']
            image = secure_filename(file.filename)
            file.save(os.path.join("pics", image))
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            user = User (userid, username, firstname, lastname, age, sex, image, created_at)
            db.session.add(user)
            db.session.commit()
            
            flash ('User' + username + 'sucessfully added!')
            return redirect (url_for('add_profile'))
            
    return render_template('add_profile.html', form=form)
    
    
    
        
@app.route('/profiles/', methods = ['GET', 'POST'])
def list_profile():
    
    all_users = db.session.query(User).all()
    users = []
    for user in all_users:
        users.append({"username":user.username, "userid":user.userid})
    if request.headers['Content-Type']=='application/json' or request.method == 'POST':
        return jsonify(users=users)
    return render_template('profiles.html', users=users)
    # return "list of profiles"

@app.route('/profile/<int:userid>')
def view_profile(userid):
    users= db.session.query(User).filter_by(userid=userid).first() 
    
    
    # # users= db.session.query(User).all()
    # # USER = []
    # # for user in users:
    # #     USER.append({"username":USER.username, "userid":USER.userid, "image":USER.image, "sex":USER.sex, "age":USER.age, "created_at":USER.created_at})
        
    # if request.headers['Content-Type']=='application/json' or request.method == 'POST':
    #         return jsonify(USER=USER)
        
    return render_template('view_profile.html', profile=users)

    
    
@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
