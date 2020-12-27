# -*- coding: utf-8 -*-

from django.http import HttpResponse
from faceMask.models import Image


# 数据库操作
def testdb(request):
    # 初始化
    response = ""
    response1 = ""

    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = Image.objects.all()

    # filter相当于SQL中的WHERE，可设置条件过滤结果
    response2 = Image.objects.filter(imageid=1)

    # 获取单个对象
    response3 = Image.objects.get(imageid=1)

    # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    #Image.objects.order_by('imageid')[0:2]

    # 数据排序
    Image.objects.order_by("imageid")

    # 上面的方法可以连锁使用
    #Image.objects.filter(name="yolov3test").order_by("imageid")

    # 输出所有数据
    for var in list:
        response1 += var.imageid + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")