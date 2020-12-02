from django.shortcuts import render        # 可以用来返回我们渲染的html文件
from django.http import HttpResponse       # 可以返回渲染的页面
from .models import Image                 # 导入我们的模型类
# Create your views here.

# 添加数据方法
def add_image(imageurl, userid, send_timestamp):
    clbc = Image.objects.get_or_create(imageurl=imageurl, userid=userid, send_timstamp=send_timestamp)

# 查询数据方法
def select_image(request):
    # 查询表中的所有数据
    rs = Image.objects.all()
    print(rs)
    # 根据筛选条件查询出表中的单挑数据（注意如果条件查询出多条数据，使用该语句会报错）
    rs1 = Image.objects.get(imageid='')
    print(rs1)
    # 根据筛选条件查询出表中的数据（可查询出多条）
    rs2 = Image.objects.filter(imageid='')
    rs2 = list(rs2)
    print(rs2)
    return HttpResponse("查询数据成功")

# 更新数据方法
def update_image(request):
    # 根据条件查询后再修改再保存
    clbc = Image.objects.get(imageid='')
    clbc.food_star = '难吃'
    clbc.save()
    # 直接修改所有的数据
    Image.objects.all().update(imageid='')
    return HttpResponse("修改数据成功")

# 删除数据方法
def delete_image(request):
    Image.objects.get(imageid='').delete()
    return HttpResponse("删除数据成功")