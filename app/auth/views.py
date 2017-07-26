from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from . import auth
from .forms import RegistForm, LoginForm, Change_Password_Form, PasswordResetRequestForm, PasswordResetForm, ChangeEmailRequestForm
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
        flash('注册成功，账户确认邮件已发送至邮箱')
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
        flash('无效的用户名或密码')
    return render_template("auth/login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('auth/account.html', current_time=datetime.utcnow())


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = Change_Password_Form()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            flash('密码已修改')
            return redirect(url_for('main.index'))
        flash('旧密码错误')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('重置密码邮件已发送至邮箱')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('密码已重置')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('账户已确认')
    else:
        flash('确认链接无效或已过期')
    return redirect(url_for('main.index'))


# 屏蔽过滤，仅在 account 页面提示未认证
# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated \
#             and not current_user.confirmed \
#             and request.endpoint[:5] != 'auth.' \
#             and request.endpoint != 'static':
#         return redirect(url_for('auth.unconfirmed'))


# @auth.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect(url_for('main.index'))
#     return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认账户', 'auth/email/confirm',
               user=current_user, token=token)
    flash('新的确认邮件已发送')
    return redirect(url_for('main.index'))


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailRequestForm()
    if form.validate_on_submit():
        new_email = form.new_email.data
        token = current_user.generate_change_email_token(new_email)
        send_email(new_email, 'Change Email', 'auth/email/change_email',
                   user=current_user, token=token, next=request.args.get('next'))
        flash('确认邮件已发送至新邮箱')
        return redirect(url_for('auth.account'))
    return render_template('auth/change_email.html', form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('邮箱已更改')
    else:
        flash('确认链接无效或已过期')
    return redirect(url_for('main.index'))
