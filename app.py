#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm  # Form 已弃用
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret_key string'
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    """docstring for NameForm"""
    name = StringField("What's your name?", validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    # name = None  # 初始置 name 为空，使用 session 时可忽略，查找为空时自动返回 None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        # form.name.data = ''
        return redirect(url_for('index'))  # 重定向至 index
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))


@app.route('/about/')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
