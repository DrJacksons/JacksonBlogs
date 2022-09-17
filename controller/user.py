import hashlib, re

from flask import Blueprint, session, make_response, request, redirect

from module.credit import Credit
from module.users import Users
from common.utility import ImageCode, gen_email_code, send_email
from logger import Logger

user = Blueprint("user", __name__)

@user.route('/vcode')
def vcode():
    code, bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    return response

# 邮箱验证码
@user.route('/ecode',methods=['POST'])
def ecode():
    email = request.form.get('email')
    if not re.match('.+@.+\..', email):
        return "email-invalid"
    code = gen_email_code()
    try:
        send_email(email, code)
        session['ecode'] = code  # 将生成的验证码保存到session
        return "send-pass"
    except:
        return "send-fail"

# 注册
@user.route('/reg',methods=['POST'])
def register():
    # 从前端返回的表单数据中获取参数
    try:
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        ecode = request.form.get('ecode').strip()
        Logger.info("正在注册新用户...")
        # 校验邮箱验证码是否正确
        if ecode != session.get('ecode'):
            return "ecode-error"

        # 验证邮箱地址和密码的正确性
        if not re.match('.+@.+\..', username) or len(password) < 5:
            return 'up-invalid'

        # 验证用户是否已经注册
        elif len(Users().find_by_username(username)) > 0:
            return "user-repeated"
        else:
            # 密码用md5加密输出
            password = hashlib.md5(password.encode()).hexdigest()
            result = Users().do_reg(username,password)
            Logger.info("注册完成！")
            # 设置session
            session['islogin'] = 'true'
            session['username'] = username
            session['nickname'] = username.split('@')[0]
            session['role'] = result.role
            # 更新积分明细表
            Credit().insert_detail(type='用户注册', target='0', credit=50)
            return 'reg-pass'
    except Exception as e:
        Logger.error(e)

@user.route('/login',methods=['POST'])
def login():
    user = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()   # 返回的是None
    vcode = request.form.get('vcode').strip()

    # 校验图形验证码是否正确
    # print("session得到的验证码：%s"%(session.get('vcode')))
    if vcode.lower() != session.get('vcode') and vcode != '0000':
        return "vcode-error"

    else:
        # 实现登录功能
        # 密码使用md5加密输出
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.find_by_username(username)
        if len(result) == 1 and result[0].password == password:
            session['islogin'] = 'true'
            session['userid'] = result[0].userid
            session['username'] = username
            session['nickname'] = result[0].nickname
            session['role'] = result[0].role
            # 更新积分明细表
            Credit().insert_detail(type='用户登录',target='0',credit=1)
            user.update_credit(1)
            Logger.info("{}完成登录.".format(result[0].nickname))
            return 'login-pass'
        else:
            return 'login-fail'

@user.route('/logout',methods=['GET'])
def logout():
    # 清空session
    Logger.info("{}已退出.".format(session['nickname']))
    session.clear()
    return redirect('/')
