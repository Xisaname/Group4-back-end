import base64
import json
import os
import datetime
from yolov3test.views import *
from django.http import HttpResponse


def hello(request):
    return HttpResponse("Hello world ! ")


def detect(request):
    imageurl = "source/2.png"
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    work_dir = os.path.join(parent_dir, "yolov3-archive")
    os.chdir(work_dir)
    command = "python detect.py --cfg cfg/yolov3-tiny.cfg --names data/coco.names --weights weights/best.pt" \
              " --source " + imageurl + " --output output"
    os.system(command)

    out_imageurl = "output\\" + imageurl.split("/")[-1]
    userid = 1
    #print(out_imageurl)
    send_time = datetime.datetime.now()
    #add_image(out_imageurl, userid, send_time)

    #imagepath = os.path.join(work_dir, out_imageurl)
    #with open(imagepath, "rb") as f:
    #    image_data = base64.b64encode(f.read()).decode()

    result = {"code": 0, "msg": "detect!", "image": 1}
    return HttpResponse(json.dumps(result), content_type="application/json")
