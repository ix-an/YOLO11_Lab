"""
SystemController：该文件只做关于页面如何访问的接口定义
接口的定义，本质上就是一个函数，格式如下：
def 函数名(request):
    return render(request, 页面访问路径)

render：django 提供的页面访问函数，用于渲染模板并返回 HttpResponse 对象
request：请求对象，包含了客户端发送的所有信息
页面访问路径：起始位置为 templates 文件夹

推荐写法：
    如果想要定义一个访问某个页面的接口，函数名 go_页面名
"""

from django.shortcuts import render  # 引入 render 函数


# login.html -> 通过访问该接口，访问登录页面
def go_login(request):
    return render(request, 'login.html')

# index.html -> 通过访问该接口，访问主页面
def go_index(request):
    return render(request, 'index.html')

# welcome.html -> 通过访问该接口，访问欢迎页面
def go_welcome(request):
    return render(request, 'welcome.html')

# detectImg.html -> 通过访问该接口，访问图片检测页面
def go_detect(request):
    return render(request, 'detect.html')

# record.html -> 通过访问该接口，访问记录页面
def go_record(request):
    return render(request, 'record.html')

# video.html -> 通过访问该接口，访问视频检测页面
def go_video(request):
    return render(request, 'video.html')

# realtime.html -> 通过访问该接口，访问实时监测页面
def go_realtime(request):
    return render(request, 'realtime.html')
