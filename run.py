#运行环境要求: Python3

import urllib
import urllib.parse
import urllib.request
import http.cookiejar
import re
import platform

import pytesseract
from PIL import Image

print("使用本软件所造成的一切后果均由使用者承担")
confirm = input("输入yes代表您同意上述说明:")
if (confirm != "yes"):
    exit()

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
#先获取cookies
CaptchaUrl = "http://jwzx.hrbust.edu.cn/academic/getCaptcha.do"
picture = opener.open(CaptchaUrl).read()
#将图片存入指定位置
if platform.system() == "Windows":
    path = r"C:\HRBUST\"
    if (os.path.exists(path)==False):
        os.mkdir(path)
    imgpath = r'C:\HRBUST\image.jpg'
else :
    imgpath = '/tmp/image.jpg'
local = open(imgpath , 'wb')
local.write(picture)
local.close()
#Windows手动输入，Linux自动识别(成功率较低，更换为深度学习算法进行识别较好，可惜我不会弄Orz)
if platform.system() == "Windows":
    import msvcrt
    import cv2
    img = cv2.imread(imgpath)
    win = cv2.namedWindow('captcha', flags=0)
    cv2.imshow('captcha', img)
    cv2.waitKey(0)
    code = raw_input('输入验证码：')
else :
    image = Image.open(imgpath)
    number = pytesseract.image_to_string(image)
    code = number

#构造post个人信息 username是学号  password是密码
postdata=urllib.parse.urlencode({
    'groupId':'',
    'j_username':'',
    'j_password':'',
    'j_captcha': code
}).encode(encoding='UTF8')

#构造post选课信息 pcourseid是课程编号
postdata2=urllib.parse.urlencode({
    'sub':'',
    'pcourseid':'',
    'seq':'1',
    'propSc': '2',
    'captchaCode':'',
}).encode(encoding='UTF8')
#登陆请求
req = urllib.request.Request(
    url = 'http://jwzx.hrbust.edu.cn/academic/j_acegi_security_check', 
    data = postdata
)

result = opener.open(req)


for item in cookie:
    print('Cookie:Name = '+item.name)
    print('Cookie:Value = '+item.value)


#选课请求
req2 = urllib.request.Request(
    url = 'http://jwzx.hrbust.edu.cn/academic/manager/electcourse/scaddaction.do',
    data = postdata2
)

result2 = opener.open(req2)

print("选课完成")

