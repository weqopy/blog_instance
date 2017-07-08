#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm  # Form 已弃用
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret_key string'
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    """docstring for NameForm"""
    name = StringField("What's your name?", validators=[DataRequired()])
    password = PasswordField('Set your password.',
                             validators=[DataRequired(),
                                         EqualTo('confirm_password',
                                         message='Passwords must match.')])
    confirm_password = PasswordField('Confirm the password', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    # name = None  # 初始置 name 为空，使用 session 时可忽略，查找为空时自动返回 None
    form = NameForm()
    if form.validate_on_submit():
        # 先取出 session 中保存的 name 变量，再进行对比
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Oh, you changed your name!', category='info')
        else:
            flash('Hello again.', category='info')
        session['name'] = form.name.data
        session['password'] = form.password.data
        # form.name.data = ''
        # 重定向至 index
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name')
                           )


@app.route('/about/')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
