import base64
import json
import os
import cv2
import datetime
import numpy as np

from yolov3test import models
from yolov3test.views import *
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
    user = 111 #request.POST.get('name')
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
    url = "yolov3-archive\\source\\" + filename + ".jpg"
    print(url)
    imgdata = base64.b64decode(file) #解码成图片并存储
    f = open(url, "wb")
    f.write(imgdata)
    f.close()
    #存储到数据库
    image = models.Image(imageurl=url, userid=user, send_timstamp=datetime.datetime.now())
    image.save()
    #ctx = {}
    #ctx['result'] = result
    if image != None:
        result = "上传成功，正在分析"
    else:
        result = "上传失败"
    result = detect(url)

    return HttpResponse(json.dumps(result), content_type="application/json")


def detect(imageurl):
    #imageurl = select_image(imageid=)
    #确定当前目录和父目录
    imageurl = imageurl.split("\\")[-1]
    source_imageurl = "source\\" + imageurl
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    work_dir = os.path.join(parent_dir, "yolov3-archive")
    os.chdir(work_dir)
    command = "python detect.py --cfg cfg/yolov3-tiny.cfg --names data/coco.names --weights weights/best.pt" \
              " --source " + source_imageurl + " --output output_dir"
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
    # add_image(out_imageurl, userid, datetime.datetime.now())

    with open(imagepath, "rb") as f:
        image_data = f.read()
        image_data = base64.b64encode(image_data).decode()
        f.close()
    result = {"code": 0, "msg": "detect!", "image": image_data}
    return result
