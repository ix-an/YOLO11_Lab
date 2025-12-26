"""
无人机检测（图片检测）控制器层
"""

from service import DroneService as ds
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from myutils.CameraUtil import CameraUtil
import os

# 图片检测
def detect_img(request):
    # --- 1. 处理 OPTIONS 预检请求 ---
    if request.method == 'OPTIONS':
        response = HttpResponse()
        # 必须添加的 CORS 头部
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    # --- 2. 处理 POST 请求 ---
    if request.method == 'POST':
        # 获取图片
        file = request.FILES.get('file')
        # 判断文件是否为空
        if not file:
            return JsonResponse({
                "status": 400,
                "msg": "上传文件不能为空",
            })
        # 取出用户名
        username = request.POST.get('username')
        # 执行检测
        return JsonResponse(ds.detect_img(file, username))
    return JsonResponse({
        "status": 405,
        "msg": "请求方式错误",
    })


# 查询图片检测记录（控制器层：得到客户端 的请求参数 -> 调用服务层 -> 返回结果）
def query_records(request):
    # --- 1. 处理 OPTIONS 预检请求 ---
    if request.method == 'OPTIONS':
        response = HttpResponse()
        # 必须添加的 CORS 头部
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    # request.GET.get 得到的内容是一个字符串
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 5))
    username = request.GET.get("username")
    return JsonResponse(ds.query_records(page, size, username))


# 摄像头检测
def detect_camera(request):
    # --- 1. 处理 OPTIONS 预检请求 ---
    if request.method == 'OPTIONS':
        response = HttpResponse()
        # 必须添加的 CORS 头部
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    # --- 2. 处理 POST 请求 ---
    if request.method == 'GET':
        # 获取是否打开摄像头参数
        is_open = request.GET.get('isOpen')
        if is_open == "true":
            """ 调用打开摄像头方法 """
            CameraUtil.open_camera()
            # 通过流式输出返回，实时的返回当前摄像头读取到的内容
            return StreamingHttpResponse(
                streaming_content=CameraUtil.detect(),
                content_type="multipart/x-mixed-replace; boundary=frame"
            )
        else:
            """ 调用关闭摄像头方法 """
            CameraUtil.close_camera()
            return JsonResponse({
                "status": 200,
                "msg": "摄像头关闭成功",
            })


# 视频检测 ------------------------------
# 上传文件和保存
def upload_video(request):
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    # 上传：POST请求
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({
            "status": 400,
            "msg": "上传文件不能为空"
        })

    # 调用服务层方法，保存视频文件
    file_path = ds.upload_video(file)
    return JsonResponse({
        "status": 200,
        "msg": "视频上传成功",
        "file_path": file_path,
    })


# 获取文件存储路径，并检测
def detect_video(request):
    """
    接收文件路径，打开文件，返回检测的MJPEG 流。
    此视图将作为前端 <img> 标签的 src
    """
    if request.method == 'OPTIONS':
        response = HttpResponse()
        # 必须添加的 CORS 头部
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    # 获取视频：GET 请求
    if request.method == 'GET':
        # 获取视频文件路径参数
        file_path = request.GET.get('file_path')
        # 判断文件路径是否为空
        if not file_path:
            return JsonResponse({
                "status": 400,
                "msg": "文件路径不存在，请检查文件上传是否成功",
            })
        # 通过流式输出返回，实时的返回当前视频帧的检测内容
        return StreamingHttpResponse(
            streaming_content=ds.detect_video(file_path),
            content_type="multipart/x-mixed-replace; boundary=frame"
        )

    # 处理其他请求：防止 Django因为函数返回 None而抛出 500错误
    return JsonResponse({
        "status": 405,
        "msg": f"请求方式错误，请使用 POST 方法上传视频文件。当前方法：{request.method}",
    })