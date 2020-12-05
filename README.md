# Group4后端项目部
2020秋季学期软件工程口罩识别项目<br>
[数据传输桥](https://github.com/Xisaname/TestBridge)
<br>
---
## 项目框架
后端项目采用[Django](https://github.com/django/django) 框架，使用[Pycharm](https://www.jetbrains.com/pycharm/) 集成开发工具
<br>
[Django说明文档](https://docs.djangoproject.com/en/3.1/)
<br>

[Django教程](https://www.runoob.com/django/django-tutorial.html)
## 环境搭建
+ Django只支持MySQL5.7以上的版本，如需使用数据库，请升级到此版本以上，以免引起不必要的麻烦
<br>
+ 个人在导包的时候更推荐在控制台使用pip工具直接从官网或GitHub导到本地，不推荐使用pycharm中的setting选项，因为这样做有时会出现错误
+ [关于pip的使用方法](https://pip.pypa.io/en/stable/)
+ 强烈建议将所有的包集成到Python3*_64/Scripts文件夹下，并将此路径导入到系统路径中

## 一些问题及解决方法
+ Q：Django自带CRSF认证机制，用来防止伪响应，但带来了一个问题：当进行post提交数据时，如果不附加该证书，会报错，且数据不会被传递。
<br>A：1. 不用post方法提交数据，改用get。但这样只能传小数据，对于大的数据，会报错 2. 在有数据交换的页面添加{{% crsf %}},但当我们用JavaScript时，例如传Ajax或者json时就会出现问题 3. 将setting.py中的```'django.middleware.csrf.CsrfViewMiddleware',```代码注释掉，目前来看，这样的方法效果比较乐观
+ Q：除了Navicat，还有没有其他的数据库管理工具
<br>A：如果你用pycharm,恭喜你，在页面的右栏写着"Database"，可以直接连接并管理你的数据库，相比于Navicat，pycharm自带的数据库功能更全，界面更酷，管理更方便，也更集成,方便Mybatis和flyway等各种数据库管理插件使用
<br>
## 部分代码展示
```python
def receive(request):
    #获取前端参数
    if request.method == "GET":
        print("method is GET")
        return render(request, "index.html")
    #获取文件，格式为base64
    fileFromPost = request.POST.get('filePath')
    #获取用户id(目前写死，留出升级空间)
    user = 111#request.POST.get('name')
    print("--------------------GET---------------------------")
    #根据base64格式，只截取数据部分
    piece= 0
    for i in range(50):
        if fileFromPost[i]==',':
            piece = i
            break
    file= fileFromPost[piece:len(fileFromPost):1]
    #命名文件的方式，先哈希，再强转成字符串存储
    filename=str(hash(file[2000:2010:1]))
    url = "sample\\" + filename + ".jpg"#后期可根据base64实际格式修改
    imgdata = base64.b64decode(file)#解码成图片并存储
    f = open(url, "wb")
    f.write(imgdata)
    f.close()
```
<br>
<br>
<br>
## 有关更多项目细节，我们将在项目发布后进行分享~~~
