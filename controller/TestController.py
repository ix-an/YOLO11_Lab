"""
测试接收请求和响应json数据给前端
    1. 服务器响应json数据给前端，可以使用两个类
        1.1 HttpResponse类：默认以文本字符串的形式返回数据
            参数1：一个json字符串（手动转换）
            参数2：content_type='application/json'
        1.2 JsonResponse类：默认把一个dict转为json返回
            参数：一个字典
"""

from django.http import JsonResponse, StreamingHttpResponse
import json
import time
from my_server.settings import BASE_DIR
import os


# get请求：获取前端传过来的 msg参数
def get_test(request):
    """
    获取请求方式： request.method，返回值为前端发送的请求方式，如GET、POST等
    获取get请求的参数： request.GET.get('参数名', 默认值)
    """
    # 获取请求方式
    method = request.method
    print("请求方式：", method)
    # 获取get请求的参数
    msg = request.GET.get('msg', '默认值')
    print("msg参数的值：", msg)
    # 返回json数据
    return JsonResponse({
        'status': 200,
        'msg': 'get请求成功',
        'data': msg
    })

# post请求：获取前端传过来的 json数据【这个数据在http请求的请求体中】
def post_test(request):
    method = request.method
    if method == 'POST':
        # 获取 post请求的json数据
        body = request.body
        """
        json.loads()：json字符串 -> python字典
        json.dumps()：python字典 -> json字符串
        """
        data = json.loads(body)
        username = data.get('username', 'admin')
        password = data.get('password', '123456')
        print("用户名：", username)
        print("密码：", password)
        # 返回json数据
        return JsonResponse({
            'status': 200,
            'msg': 'post请求成功',
        })
    else:
        return JsonResponse({
            'status': 405,
            'msg': '请求方式错误',
        })


# post请求：上传文件
def post_file(request):
    method = request.method
    if method == 'POST':
        # 判断文件是否为空
        if not request.FILES.get('file'):
            return JsonResponse({
                'status': 400,
                'msg': '文件不能为空',
            })
        # 获取文件对象
        file = request.FILES.get('file')
        # 通过当前时间戳设置文件名
        filename = str(int(time.time())) + '.jpg'
        # 把得到的文件写入 static/upload 中
        save_path = os.path.join(BASE_DIR, 'static/upload',  filename)
        with open(save_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        return JsonResponse({
            'status': 200,
            'msg': '上传成功',
        })

    return JsonResponse({
        'status': 405,
        'msg': '请求方式错误',
    })


# 流式输出
# 1. 创建一个生成数据的函数，用yield返回
def generator():
    for i in range(5):
        yield f'the {i} times outputs\n'
        time.sleep(1)  # 模拟耗时

# 2. 接口函数
def post_stream(request):
    return StreamingHttpResponse(
        streaming_content=generator(),
        content_type='text/plain'
    )
