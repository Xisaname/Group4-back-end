import base64
import hashlib
import json
import os
import cv2
import datetime
import numpy as np
from PIL import Image

from faceMask import models
from faceMask.views import *
from django.http import HttpResponse
import sys
sys.path.append("D:/Study/2020秋/软件工程/djangoProject/yolov3-archive")
from yolov3 import *

yolo = yolov3(runpath="D:/Study/2020秋/软件工程/djangoProject")

def hello(request):
    return HttpResponse("Hello world !")


def receive(request):
    # 获取前端参数
    if request.method == "GET":
        print("method is GET")
        return HttpResponse({"code": 1, "msg": "error!"}, content_type="application/json")
    # 获取文件，格式为base64
    fileFromPost = request.POST.get('filePath')
    # 获取用户id
    userid = int(request.POST.get('userid'))

    print("--------------------RECEIVE--------------------")
    print(len(fileFromPost))
    # 根据base64格式，只截取数据部分
    piece = 0
    for i in range(50):
        if fileFromPost[i] == ',':
            piece = i
            break
    file = fileFromPost[piece:len(fileFromPost):1]
    # 命名文件的方式
    filename = str(hash(file[2000:2010:1]))
    imageurl = "yolov3-archive\\source\\" + filename + ".jpg"
    imgdata = base64.b64decode(file)  # 解码成图片并存储
    with open(imageurl, "wb") as f:
        f.write(imgdata)
        f.close()
    result = detect_image(userid, imageurl)
    return HttpResponse(json.dumps(result), content_type="application/json")


def detect_image(userid, imageurl):
    # 读取存储图片
    image = cv2.imdecode(np.fromfile(os.path.join(imageurl), dtype=np.uint8), cv2.IMREAD_COLOR)
    with torch.no_grad():
        outImage = yolo.detect_image(image)
    # 图片压缩
    imSize = outImage.shape
    rate = float(imSize[0]) / (imSize[0] + imSize[1])
    outImage = cv2.resize(outImage, (int(1000 - 1000 * rate), int(rate * 1000)))
    # 保存图片
    save_path = os.path.join("result", imageurl.split("\\")[-1])
    cv2.imwrite(save_path, outImage)
    # 写入数据库
    if userid != -1:
        add_image(save_path, userid, datetime.datetime.now())
    # 读取结果并转换为base64格式进行传输
    with open(save_path, "rb") as f:
        image_data = f.read()
        image_data = base64.b64encode(image_data).decode()
        f.close()
    result = {"code": 0, "msg": "detect!", "image": image_data}
    return result


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
    cv2.resize(img, (img.size, img.size))
    cv2.imencode('.jpg', img)[1].tofile(save_dir)

    #写入数据库
    # print(out_imageurl)
    add_image(save_dir, userid, datetime.datetime.now())

    with open(save_dir, "rb") as f:
        image_data = f.read()
        image_data = base64.b64encode(image_data).decode()
        f.close()
    result = {"code": 0, "msg": "detect!", "image": image_data}
    return result


def user_images(request, cv=None):
    # 获取用户
    user_id = int(request.POST.get('userid'))
    # 根据用户获取图片
    _images = models.Image.objects.filter(userid=user_id)
    images = []
    length = 0
    # 遍历插入图片到字典中
    for _image in _images:
        length += 1
        f = open(_image.imageurl, 'rb')
        image_pure_data = base64.b64encode(f.read()).decode()  # 强转成图片格式
        image_data = 'data:image/jpg;base64,' + image_pure_data
        image = {'url': _image.imageurl, "image": image_data}
        images.append(image)
        f.close()
    result = {"user_id": user_id, "faceMask": images, "length": length}
    # 封装成json传输
    return HttpResponse(json.dumps(result), content_type="application/json")


def user_registered(request):
    #用户注册
    userName = request.POST.get('username')
    user = models.User.objects.filter(username=userName).first()
    password = hashlib.md5(request.POST.get('password').encode(encoding='UTF-8')).hexdigest()
    if user != None:
        result = {'error_code': 1, 'msg': '该用户已存在'}
    else:
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

