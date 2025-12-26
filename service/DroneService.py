"""
图片检测服务层
"""
import json
import os
from fileinput import filename
import cv2
from my_server.settings import BASE_DIR
from ultralytics import YOLO
import time
from dao import DroneDao as dd

# 用于视频检测的模型：避免每重复加载
MODEL = YOLO(os.path.join(BASE_DIR, "weights", "yolo11s.engine"))


# 图片检测
def detect_img(file, username):
    """
    1. 接收上传图片，存入 static/upload 中
    2. 加载模型，进行检测
    3. 把检测结果的部分信息存入MySQL
    4. 返回检测结果：类别（个数统计）、置信度、检测结果图片的访问路径
    """
    # 加载模型
    model = YOLO(os.path.join(BASE_DIR, "weights", "yolo11s.engine"))
    # 生成类别计数字典：从模型中获取类别名称列表，动态生成 {类别: 0} 字典
    classes_number = {name: 0 for name in model.names.values()}

    # 设置一个新文件名，后缀改为.jpg
    filename = str(int(time.time())) + ".jpg"
    # 保存图片
    save_path = os.path.join(BASE_DIR, "static", "upload", filename)
    with open(save_path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)

    # 执行检测
    results = model.predict(
        source=save_path,
        save=True,
        project=os.path.join(BASE_DIR, "runs", "detect"),
        conf=0.5,
    )

    result_url = ""
    total_conf = 0.0
    length = 0

    for res in results:
        result_url = res.save_dir.split("detect")[-1].replace("\\", "")
        length = len(res.boxes)  # 预测结果数量

        for box in res.boxes:
            class_name = res.names[int(box.cls.item())]  # 获取类别名称
            classes_number[class_name] += 1  # 类别数量统计
            total_conf += round(box.conf.item(), 2)  # 统计置信度

    # 过滤出值非 0的类别
    non_zero_classes = {k: v for k, v in classes_number.items() if v != 0}
    # 计算平均置信度
    if length > 0:
        avg_conf = round(total_conf / length, 2)
    else:
        avg_conf = 0.0
    # 结果保存路径
    result_url = "static/detect/" + result_url + "/" + filename
    # 原始图片路径
    origin_url = "static/upload/" + filename
    """
    存储结果到MySQL：
    record_id ：自增主键
    origin_url ： 原始图片的访问路径
    result_url ：检测结果图片访问路径
    conf ：平均置信度
    result ：检测结果信息
    username ：检测人员
    create_time ：检测时间
    """
    flag = dd.save_result([origin_url, result_url, avg_conf, json.dumps(non_zero_classes), username])
    if flag:
        return {
            "status": 200,
            "msg": "检测成功",
            "data": {
                "classesNumber": non_zero_classes,
                "avgConf": avg_conf,
                "resultUrl": result_url,
            }
        }
    else:
        return {
            "status": 500,
            "msg": "检测结果保存失败",
        }


# 查询图片检测记录（服务器端 -> 分页）
def query_records(page, size, username):
    # 计算 start
    start = (page - 1) * size
    # 获取数据库查询结果
    records = dd.query_records(start, size, username)

    # 保存查询结果的列表
    records_list = []

    # 封装数据 --- 客户端需要数据格式为[{},{}...]
    for i in records:
        records_list.append({
            "id": i[0],
            "originUrl": i[1],
            "resultUrl": i[2],
            "conf": i[3],
            "classesNumber": i[4],
            "username": i[5],
            "createTime": i[6].strftime("%Y-%m-%d %H:%M:%S")  # 时间格式转换
        })
    # 获取记录总数
    total = dd.query_total(username)
    return {
        "status": 200,
        "msg": "查询成功",
        "data": {
            "records": records_list,
            "total": total,
        }
    }


# 上传视频文件并保存
def upload_video(file):
    """
    接收上传的视频文件，保存到指定目录。
    返回保存后的文件路径。
    """
    # 生成唯一文件名并保存
    file_name = str(int(time.time())) + ".mp4"
    save_path = os.path.join(BASE_DIR, "static", "upload", file_name)
    # 分块写入文件
    with open(save_path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)
    return save_path



# 视频检测（实时地把检测结果返回给客户端显示）
def detect_video(file_path):
    """
    接收已保存的视频文件路径，打开视频，进行检测。
    并以生成器形式返回检测流。
    """
    cap = None
    # 使用 OpenCV读取视频文件
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        return

    # 循环检测视频帧
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 读取失败或视频结束

        # 调用模型检测
        results = MODEL(source=frame, stream=True, verbose=False)

        annotated_frame = frame  # 检测结果帧
        for result in results:
            annotated_frame = result.plot()
            break  # 每帧只检测一次

        # 编码为 jpg格式
        ret, buffer = cv2.imencode(".jpg", annotated_frame)
        # 通过字节流返回结果
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

    # 释放资源
    cap.release()

