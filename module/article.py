from common.database import dbconnect
from sqlalchemy import Table
import time
from module.users import Users

dbsession, md, DBase = dbconnect()

class Article(DBase):
    __table__ = Table('article', md, autoload=True)

    def find_all(self):
        result = dbsession.query(Article).all()
        return result

    # 指定分页的limit和offset的参数值，同时与用户表做连接查询
    def find_limit_with_users(self, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid) \
            .filter(Article.hide == 0, Article.drafted == 0, Article.checked == 1).order_by(
            Article.articleid.asc()).limit(count).offset(start).all()
        return result

    # 统计一下当前文章的总数量
    def get_total_count(self):
        count = dbsession.query(Article).filter(Article.hide == 0, Article.drafted == 0, Article.checked == 0).count()
        return count

    # 插入一篇新的文章，草稿或投稿通过参数进行区分
    def insert_article(self, userid, type, headline, content, thumbnail, credit, drafted=0, checked=0):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        # userid = session.get('username')
        # 其他字段在数据库中均已设置好默认值，无须手动插入
        article = Article(userid=userid, category=type, headline=headline,\
                          content=content, thumbnail=thumbnail, credit=credit,\
                          drafted=drafted, checked=checked, createtime=now, updatetime=now)
        dbsession.add(article)
        dbsession.commit()
        return article.articleid  # 将新文章编号返回，便于前端页面跳转

    # 每阅读一次，阅读数+1
    def read_article(self, articleid):
        article = dbsession.query(Article).filter(Article.articleid == articleid).first()
        article.readcount += 1
        dbsession.commit()

    # 根据id查询文章  return: (Article, 'nickname')
    def find_article_by_id(self, articleid):
        row = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid) \
            .filter(Article.hide == 0, Article.drafted == 0, Article.checked == 0,
                    Article.articleid == articleid).first()
        return row

    # 根据文章类别id 返回该类别的文章
    def find_article_by_type(self, type, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users, Users.userid==Article.userid).\
            filter(Article.hide==0, Article.drafted==0, Article.checked==0, Article.category==type).\
            order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    def get_count_by_type(self, type):
        count = dbsession.query(Article).filter(Article.hide==0, Article.drafted==0, Article.checked==0, Article.category==type).count()
        return count

    # 根据文章标题进行模糊搜索
    def find_by_headline(self, headline, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid) \
            .filter(Article.hide==0, Article.drafted==0, Article.checked==0, Article.headline.like('%' + headline +'%')).\
            order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    def get_count_by_headline(self, headline):
        count = dbsession.query(Article).filter(Article.hide == 0, Article.drafted == 0, Article.checked == 0,
                                                Article.headline.like('%' + headline +'%')).count()
        return count