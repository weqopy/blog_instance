from flask import render_template, url_for, redirect, flash, session
from datetime import datetime

from . import auth
from .forms import RegistForm, LoginForm


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        session['password'] = form.password.data
        flash('You have registered.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', current_time=datetime.utcnow(), form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == session.get('username') and form.password.data == session.get('password'):
            # flash('You have loged.')
            return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)
