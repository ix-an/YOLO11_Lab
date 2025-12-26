"""
URL configuration for my_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
# 导入需要配置请求路径的文件
from controller import SystemController as sc
from controller import TestController as tc
from controller import UserController as uc
from controller import DroneController as dc

"""
    在urlpatterns配置某一个接口的请求路径
    通过path函数实现，函数两个参数：
        1、等价于 @app.get("/路径") 中的/路径
        2、等价于 @app.get("/路径") 装饰的函数
    总结：通过 path 的第一个参数（请求路径）访问到 path 的第二参数（函数、接口）
"""
urlpatterns = [
    path("admin/", admin.site.urls),
    # login.html --- http://localhost:8000/login/
    path("", sc.go_login),
    path("login/", uc.login),
    # index.html --- http://localhost:8000/index/
    path("index/", sc.go_index),
    # welcome.html --- http://localhost:8000/Welcome/
    path("welcome/", sc.go_welcome),
    # detect_img API --- http://localhost:8000/detectImg/
    path("detectImg/", dc.detect_img),
    # detect.html --- http://localhost:8000/detect/
    path("detect/", sc.go_detect),
    # record.html --- http://localhost:8000/record/
    path("record/", sc.go_record),
    # record API --- http://localhost:8000/queryRecords/
    path("queryRecords/", dc.query_records),
    # video.html --- http://localhost:8000/video/
    path("video/", sc.go_video),
    # realtime.html --- http://localhost:8000/realtime/
    path("realtime/", sc.go_realtime),
    # 摄像头检测 detect_camera API --- http://localhost:8000/detectCamera/
    path("detectCamera/", dc.detect_camera),
    # 视频检测 detect_video API --- http://localhost:8000/detectVideo/
    path("detectVideo/", dc.detect_video),
    # 视频上传 upload_video API --- http://localhost:8000/uploadVideo/
    path("uploadVideo/", dc.upload_video),


    # # test.html --- http://localhost:8000/getTest/
    # # path("getTest/", tc.get_test),
    # # # post_body --- http://localhost:8000/postBody/
    # path("postBody/", tc.post_body),
    # # # post_file --- http://localhost:8000/postFile/
    # path("postFile/", tc.post_file),
    # # # post_stream --- http://localhost:8000/postStream/
    # path("postStream/", tc.post_stream),
    # # # login --- http://localhost:8000/login/
]


