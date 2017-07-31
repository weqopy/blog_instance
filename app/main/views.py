from flask import render_template, abort
from datetime import datetime

from . import main
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", current_time=datetime.utcnow())


# 取消 url 结尾 / 符号
@main.route('/about')
def about():
    return render_template("about.html")


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
