from flask import Blueprint, render_template, request, jsonify
from module.article import Article
import time
import os
import math

from common.utility import compress_image

index = Blueprint('index', __name__)

@index.route('/')
def home():
    # choose 5 articles to show in the home page
    article = Article()
    result = article.find_limit_with_users(0,5)
    total = math.ceil(article.get_total_count() / 5)
    return render_template('index.html',result=result,total=total,page=0)

@index.route('/page/<int:page>')
def paginate(page):
    start = (page - 1) * 10
    article = Article()
    result = article.find_limit_with_users(start, 5)
    total = math.ceil(article.get_total_count() / 5)
    return render_template('index.html', result=result, total=total, page=page)


@index.route('/type/<int:typeid>-<int:page>')
def type(typeid, page):
    article = Article()
    result = article.find_article_by_type(typeid,0,5)
    count = article.get_count_by_type(typeid)
    total = math.ceil(count / 5)
    return render_template('index.html',result=result,total=total,page=page,type=typeid)

@index.route('/prepost')
def prepost():
    return render_template('article-post.html')

@index.route('/uedit',methods=['GET','POST'])
def ueditor():
    # 需要配置Ueditor的config.json配置文件
    # 根据Ueditor的接口定义规则，如果前端参数为action=config,
    # 则表示视图请求后台的config.json文件，请求成功后则说明后台接口能正常工作
    param = request.args.get('action')
    if param == 'config' and request.method == 'GET':
        return render_template('config.json')

    # 上传图片接口
    elif request.method == 'POST' and request.args.get('action') == 'uploadimage':
        f = request.files['upfile']  # 获取前端图片文件数据
        filename = f.filename

        # 为上传来的文件生成统一的文件名
        suffix = filename.split('.')[-1]
        newname = time.strftime('%Y%m%d_%H%M%S.' + suffix)
        f.save('./static/upload/' + newname)

        # 对图片进行压缩，按照1200像素宽度为准，并覆盖原始文件
        source = dest = './static/upload/' + newname
        compress_image(source, dest, 1200)

        # f.save('./static/upload/' + filename)  # 图片保存到upload目录
        result = {}  # 构造响应数据
        result['state'] = 'SUCCESS'
        result['url'] = f'/static/upload/{newname}'
        result['title'] = filename
        result['original'] = filename

        return jsonify(result)  # 以json数据格式返回响应，供前端编辑器引用

    # 列出所有图片给前端浏览
    elif request.method == 'GET' and param == 'listimage':
        list = []
        filelist = os.listdir('./static/upload')
        for filename in filelist:
            if filename.lower().endswith('.png') or filename.lower().endswith('.jpg'):
                list.append({'url': '/static/upload/%s' % filename})

        result = {}
        result['state'] = 'SUCCESS'
        result['list'] = list
        result['start'] = 0
        result['total'] = 30
        return jsonify(result)

@index.route('/search/<int:page>-<keyword>')
def search(page, keyword):
    start = (page-1)*10
    article = Article()
    result = article.find_by_headline(keyword, start, 10)
    total = math.ceil(article.get_count_by_headline(keyword)/10)

    return render_template('search.html', result=result, page=page, total=total)