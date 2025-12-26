"""
用户控制器：处理用户请求并响应
"""
from service import UserService as us
import json
from django.http import JsonResponse

# 用户登录
def login(request):
    # ✅ 1. 先处理 OPTIONS（浏览器预检）
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # ✅ 2. 再处理 POST
    if request.method == 'POST':
        # 获取请求体中的数据：用户名和密码
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        # 响应请求：调用服务层登录方法，返回结果
        return JsonResponse(us.login(username, password))