import random,string
import re
import requests
import time
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

class ImageCode():
    # 生成随机颜色
    def rand_color(self):
        red = random.randint(32,200)
        green = random.randint(5,250)
        blue = random.randint(0,200)
        return red, green, blue

    # 生成随机字符串
    def gen_text(self):
        list = random.sample(string.ascii_letters+string.digits, 4)  # 从一个大的列表或字符串中，随机获取N个字符来构建出一个字列表
        return ''.join(list)

    # 画一些干扰线，其中draw为PIL中的ImageDraw对象
    def draw_lines(self, draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=2)

    # 绘制验证码图片
    def draw_verify_code(self):
        code = self.gen_text()
        width, height = 120, 50  # 设定图片大小，可根据实际需求调整
        # 创建图片对象，并设定背景为白色
        im = Image.new('RGB', (width,height), 'white')
        # 选择使用何种字体及字体大小
        font = ImageFont.truetype(font='arial.ttf', size=40)
        draw = ImageDraw.Draw(im)
        # 绘制字符串
        for i in range(4):
            draw.text((5+random.randint(-3,3)+23*i, 5+random.randint(-3,3)),
                      text=code[i], fill=self.rand_color(), font=font)
        # 绘制干扰线
        self.draw_lines(draw, 4, width, height)
        return im, code

    # 生成图片验证码并返回给控制器
    def get_code(self):
        image, code = self.draw_verify_code()
        buf = BytesIO()
        image.save(buf, 'jpeg')
        bstring = buf.getvalue()  # 字节码
        return code, bstring

# 发送QQ邮箱验证码，参数为收件箱地址和随机生成的验证码
def send_email(receiver, ecode):
    sender = 'Jackson <178276549@qq.com>'
    content = f"<br/>欢迎注册蜗牛笔记博客系统账号，您的邮箱验证码为：<span style='color: red; font-size: 20px;'>{ecode}</span>,请复制到注册窗口完成注册，感谢您的支持。<br/>"
    # 实例化邮件对象，并指定邮件的关键信息
    message = MIMEText(content,'html','utf-8')
    # 指定邮件的标题，同样使用utf-8编码
    message['Subject'] = Header('蜗牛笔记的注册验证码', 'utf-8')
    message['From'] = sender
    message['To'] = receiver

    smtpObj = SMTP_SSL('smtp.qq.com')
    # 通过你的邮箱账号和获取到的授权码登录QQ邮箱
    smtpObj.login(user='178276549@qq.com', password='pcpobqjnwdkpcahh')
    # 指定发件人，收件人和邮件内容
    smtpObj.sendmail(sender, receiver, str(message))
    smtpObj.quit()

# 生成6位随机字符串作为邮箱验证码
def gen_email_code():
    str = random.sample(string.ascii_letters+string.digits, 6)
    return ''.join(str)

# 压缩图片，通过参数width指定压缩后的图片大小
def compress_image(source, dest, width):
    im = Image.open(source)
    x,y = im.size
    if x > width:
        # 等比例缩放
        ys = int(y * width / x)
        xs = width
        # 调整当前图片的尺寸（同时也会压缩大小）
        temp = im.resize((xs,ys), Image.ANTIALIAS)
        # 将图片保存80%的质量压缩
        temp.save(dest, quality=80)
    # 如果尺寸小于指定宽度则不缩减尺寸，只压缩保存
    else:
        im.save(dest, quality=80)

# 解析文章内容中的图片地址
def parse_image_url(content):
    temp_list = re.findall('<img src="(.+?)"', content)
    url_list = []
    for url in temp_list:
        # 如果图片为gif，则直接跳过，不对其作任何处理
        if url.lower().endswith('.gif'):
            continue
        url_list.append(url)
    return url_list

# 远程下载指定url地址的图片，并保存到临时目录中
def download_image(url, dest):
    response = requests.get(url)
    with open(file=dest, mode='wb') as f:
        f.write(response.content)

# 解析列表中的图片URL地址并生成缩略图，返回缩略图名称
def generate_thumb(url_list):
    '''
    根据URL地址解析出文件名和域名，
    通常建议使用文中内容中的第一张图片来生成缩略图
    先遍历url_list，查找里面是否存在本地上传的图片，找到即处理，代码运行结束
    '''
    for url in url_list:
        if url.startswith('/static/upload/'):
            filename = url.split('/')[-1]
            # 找到本地图片后对其进行压缩处理，设置缩略图宽度为400像素即可
            compress_image('./static/upload/' + filename, './static/thumb/'+filename, 400)
            return filename

    # 如果在内容中没有找到本地图片，则先将URL图片下载到本地再处理，直接将第一张图片作为缩略图，并生成基于时间戳的标准文件名
    url = url_list[0]
    filename = url.split('/')[-1]
    suffix = filename.split('.')[-1]  # 获取后缀
    thumbname = time.strftime('%Y%m%d_%H%M%S.' + suffix)
    download_image(url, './static/download/'+thumbname)
    compress_image('./static/upload/' + thumbname, './static/thumb/'+thumbname, 400)

    return thumbname