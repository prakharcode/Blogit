from app import app, db,g
from flask import render_template, request,url_for, flash, redirect
from forms import LoginForm, SignUpForm
from flask_login import login_user, logout_user,login_required


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/')
@login_required
def homepage():
    return render_template('homepage.html')

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            login_user(form.user, remember = form.remember_me.data)
            flash('Successfully Logged In as %s!'%form.user.email, 'success')
            return redirect(url_for('homepage'))
    else:
        form = LoginForm()
    return render_template('login.html', form =form)
@app.route('/signup/', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = SignUpForm(request.form)
        if form.validate():
            user = form.save_entry()
            db.session.add(user)
            db.session.commit()
            flash('User %s created Successfully! Please Login'% user.name,'success')
            return redirect(url_for('login'))
    else:
        form = SignUpForm()
    return render_template('signup.html',form = form)

@app.route('/logout/')
def logout():
    logout_user()
    flash('You logged out!','success')
    return redirect(url_for('index'))
