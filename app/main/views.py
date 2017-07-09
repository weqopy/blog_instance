from flask import render_template, session, redirect, url_for, flash
from datetime import datetime

from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
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
        return redirect(url_for('.index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name')
                           )
