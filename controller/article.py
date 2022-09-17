from flask import Blueprint, render_template, abort, session, request

from common.utility import parse_image_url, generate_thumb
from module.article import Article
from module.users import Users

article = Blueprint("article", __name__)


@article.route('/article/<int:articleid>')
def read(articleid):
    try:
        # result返回的数据格式:(Article,'nickname'),所以获取Article是result[0]
        result = Article().find_article_by_id(articleid)
        if result is None:
            abort(404)
    except:
        abort(500)

    Article().read_article(articleid)
    return render_template('article-user.html', result=result)

@article.route('/article', methods=['POST'])
def add_article():
    headline = request.form.get('headline')
    content = request.form.get('content')
    type = int(request.form.get('type'))
    credit = int(request.form.get('credit'))
    drafted = int(request.form.get('drafted'))
    checked = int(request.form.get('checked'))

    if session.get('username') is None:
        return 'perm-denied'
    else:
        user = Users().find_user_by_id(session.get('username'))
        if user.role == 'editor':
            # 权限合格，可以执行发布文章的代码
            # 首先为文章生成缩略图，优先从内容中找，找不到则随机生成一张
            url_list = parse_image_url(content)
            if len(url_list) > 0:
                thumbname = generate_thumb(url_list)
            else:
                # 如果文章中没有图片，则根据文章类别指定一张缩略图
                thumbname = '%d.png' % type
            try:
                userid = user.userid
                id = Article().insert_article(userid=userid,type=type,headline=headline,content=content,thumbnail=thumbname,credit=credit,drafted=drafted,checked=checked)
                return str(id)
            except Exception as e:
                return 'post-fail'
        # 如果角色不是作者，则只能投稿，不能正式发布
        elif checked == 1:
            return 'perm-denied'
        else:
            return 'perm-denied'