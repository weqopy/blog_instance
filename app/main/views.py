from flask import render_template
from datetime import datetime

from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", current_time=datetime.utcnow())


# 取消 url 结尾 / 符号
@main.route('/about')
def about():
    return render_template("about.html")
