import random

from flask import session
from common.database import dbconnect
from sqlalchemy import Table
import time

dbsession, md, DBase = dbconnect()

class Users(DBase):
    __table__ = Table('users', md, autoload=True)

    def find_by_username(self, username):
        result = dbsession.query(Users).filter(Users.username==username).all()
        return result

    def find_user_by_id(self, userid):
        row = dbsession.query(Users).filter(Users.username==userid).first()
        return row

    # 用户注册只支持文章阅读权限（user）
    def do_reg(self, username, password):
        now = time.strftime("%Y-%m-%d, %H:%M:%S")
        nickname = username.split('@')[0]
        avatar = str(random.randint(1, 15))
        user = Users(username=username,password=password,role='user',credit=50,nickname=nickname,
                     createtime=now,updatetime=now,avatar=avatar+'.png')
        dbsession.add(user)
        dbsession.commit()
        return user

    # 修改用户剩余积分，积分为正数表示增加积分，为负数表示减少积分
    def update_credit(self, credit):
        user = dbsession.query(Users).filter_by(username=session.get('username')).one()
        user.credit = int(user.credit) + credit
        dbsession.commit()