from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from . import auth
from .forms import RegistForm, LoginForm, Change_Password_Form
from .. import db
from ..models import User
from ..email import send_email


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认账户', 'auth/email/confirm',
                   user=user, token=token)
        flash('You have registered, a confirmation email has been sent to you by email.')
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


# TODO: 通过邮件修改密码
# TODO: 修改邮箱
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


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('Confirmed!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


# TODO: 分析逻辑
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认账户', 'auth/email/confirm',
               user=current_user, token=token)
    flash('新的确认邮件已发送')
    return redirect(url_for('main.index'))
