import base64
import hashlib
import json
import os

import cv2
import datetime
import numpy as np

from faceMask import models
from faceMask.views import *
from django.http import HttpResponse


def hello(request):
    return HttpResponse("Hello world !")


def receive(request):
    #获取前端参数
    if request.method == "GET":
        print("method is GET")
        return HttpResponse({"code": 1, "msg": "error!"}, content_type="application/json")
    #获取文件，格式为base64
    fileFromPost = request.POST.get('filePath')
    #获取用户id
    userid = int(request.POST.get('userid'))

    print("--------------------GET---------------------------")
    print(len(fileFromPost))
    #根据base64格式，只截取数据部分
    piece = 0
    for i in range(50):
        if fileFromPost[i] == ',':
            piece = i
            break
    file = fileFromPost[piece:len(fileFromPost):1]
    #命名文件的方式
    filename = str(hash(file[2000:2010:1]))
    print(filename)
    imageurl = "yolov3-archive\\source\\" + filename + ".jpg"
    print(imageurl)
    imgdata = base64.b64decode(file) #解码成图片并存储
    f = open(imageurl, "wb")
    f.write(imgdata)
    f.close()
    #存储到数据库
    #image = models.Image(imageurl=imageurl, userid=userid, send_timstamp=datetime.datetime.now())
    #image.save()
    #ctx = {}
    #ctx['result'] = result
    #if image != None:
    #    result = "上传成功，正在分析"
    #else:
    #    result = "上传失败"
    result = detect(userid, imageurl)

    return HttpResponse(json.dumps(result), content_type="application/json")


def detect(userid, imageurl):
    #imageurl = select_image(imageid=)
    #确定当前目录和父目录
    imageurl = imageurl.split("\\")[-1]
    source_imageurl = "source\\" + imageurl
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    work_dir = os.path.join(parent_dir, "yolov3-archive")
    os.chdir(work_dir)
    command = "python detect.py --cfg cfg/yolov3-tiny.cfg --names data/coco.names --weights weights/best.pt" \
              " --source " + source_imageurl + " --output output_dir --save-txt"
    os.system(command)
    os.chdir('../')

    out_imageurl = "output_dir\\" + imageurl
    imagepath = os.path.join(work_dir, out_imageurl)

    # 保存图片
    save_dir = os.path.join(parent_dir, "result", imageurl)
    img = cv2.imdecode(np.fromfile(imagepath, dtype=np.uint8), flags=cv2.IMREAD_COLOR)
    cv2.imencode('.jpg', img)[1].tofile(save_dir)

    #写入数据库
    # print(out_imageurl)
    add_image(save_dir, userid, datetime.datetime.now())

    with open(imagepath, "rb") as f:
        image_data = f.read()
        image_data = base64.b64encode(image_data).decode()
        f.close()
    result = {"code": 0, "msg": "detect!", "image": image_data}
    return result


def user_images(request, cv=None):
    user_id = int(request.POST.get('userid'))
    #user_id=111
    _images = models.Image.objects.filter(userid=user_id)
    images = []
    length = 0
    for _image in _images:
        length += 1
        f = open(_image.imageurl, 'rb')
        image_pure_data = base64.b64encode(f.read()).decode() #强转成图片格式
        image_data = 'data:image/jpg;base64,' + image_pure_data
        image = {'url': _image.imageurl, "image": image_data}
        images.append(image)
    result = {"user_id": user_id, "images": images, "length": length}
    #print(result["images"][0]["image"])
    #cv.namedWindow('IMG')
    #return "ok"
    return HttpResponse(json.dumps(result), content_type="application/json")


def user_registered(request):
    #用户注册
    userName = request.POST.get('username')
    user = models.User.objects.filter(username=userName).first()
    password = hashlib.md5(request.POST.get('password').encode(encoding='UTF-8')).hexdigest()
    if user != None:
        print("到达这里了")
        result = {'error_code': 1, 'msg': '该用户已存在'}
    else:
        print("到达else了")
        user = models.User(username=userName, password=password)
        user.save()
        User = models.User.objects.filter(username=userName).first()
        result = {'error_code': 0, 'msg': '注册成功', 'data': {'userid': User.userid, 'username': User.username}}
    print(result)
    return HttpResponse(json.dumps(result), content_type="application/json")


def user_getin(request):
    #用户登录
    userName = request.POST.get('username')
    user = models.User.objects.filter(username=userName).first()
    if user == None:
        result = {'error_code': 1, 'msg': '该账号不存在，请注册'}
    else:
        password = hashlib.md5(request.POST.get('password').encode(encoding='UTF-8')).hexdigest()
        if user.password == password:
            result = {'error_code': 0, 'msg': '登录成功', 'data':{'userid': user.userid, 'username': user.username}}
        else:
            result = {'error_code': 2, 'msg': '密码错误，请重新输入'}
    return HttpResponse(json.dumps(result), content_type="application/json")

