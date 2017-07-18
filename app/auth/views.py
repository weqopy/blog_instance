from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from . import auth
from .forms import RegistForm, LoginForm, Change_Password_Form
from .. import db
from ..models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You have registered.')
        return redirect(url_for('auth.login'))
    return render_template("auth/register.html", current_time=datetime.utcnow(), form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template("auth/login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('auth/account.html', current_time=datetime.utcnow())


@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = Change_Password_Form()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            flash('You have changed password.')
            return redirect(url_for('main.index'))
        flash('Invalid old password')
    return render_template('auth/change_password.html', form=form)
