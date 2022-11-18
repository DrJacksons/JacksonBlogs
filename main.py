from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

from __init__  import __appname__

app = Flask(__appname__, template_folder='templates', static_folder='/', static_url_path='')

# 引入数据库，使用集成化方式
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:djk123a@localhost:3306/jacksonblogs?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'Jackson'
# 实例化db对象
db = SQLAlchemy(app)

# 定义500错误页面
@app.errorhandler(500)
def server_error(e):
    return render_template('error-500.html')

@app.errorhandler(404)
def server_error(e):
    return render_template('error-404.html')


@app.context_processor
def gettype():
    type = {
        '1': 'Python开发',
        '2': 'C++开发',
        '3': 'Go开发',
        '4': 'Web前端',
        '5': '算法',
        '6': '人工智能',
        '7': '数据库',
        '8': '其它',
    }
    return dict(article_type=type)


if __name__ == '__main__':
    from controller.index import *
    app.register_blueprint(index)

    # from controller.ueditor import *
    # app.register_blueprint(ueditor)

    from controller.user import *

    app.register_blueprint(user)

    from controller.article import *

    app.register_blueprint(article)

    from controller.other import *

    app.register_blueprint(other)

    app.run(debug=True)
