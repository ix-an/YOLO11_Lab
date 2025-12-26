"""
    摄像头检测工具，三个方法：
        1、打开摄像头 cls.open_camera
        2、关闭摄像头 cls.close_camera
        3、检测 cls.detect
    一般情况下，摄像头资源是唯一的，所以需要使用锁机制
    给资源加锁，得到钥匙的就可以访问，否则就等待
"""
from ultralytics import YOLO
import threading  # 线程锁
import cv2
import os
from my_server.settings import BASE_DIR


class CameraUtil:
    """
        摄像头检测工具类
    """
    model_path = os.path.join(BASE_DIR, "weights", "yolo11s.engine")
    model = YOLO(model_path)  # 加载模型
    lock = threading.Lock()  # 摄像头锁
    cap = None  # 摄像头对象
    active = False  # 摄像头状态

    @classmethod
    def open_camera(cls):
        """ 打开摄像头 """
        with cls.lock:  # 获取锁，才能访问摄像头（with自动释放）
            if not cls.active:
                cls.cap = cv2.VideoCapture(0)  # 打开摄像头
                if not cls.cap.isOpened():  # 打开失败
                    cls.cap = None
                    raise Exception("无法打开摄像头")
                cls.active = True  # 修改摄像头状态为打开

    @classmethod
    def close_camera(cls):
        """ 关闭摄像头 """
        with cls.lock:  # 获取锁，才能访问摄像头（with自动释放）
            if cls.active:
                cls.cap.release()  # 关闭摄像头
                cls.cap = None
                cls.active = False

    @classmethod
    def detect(cls):
        """ 检测：作为 StreamingHttpResponse 的生成器 """
        while True:
            if not cls.cap.isOpened():  # 判断摄像头是否打开
                return

           # ret：布尔值，是否成功读取到一帧， frame：当前帧
            ret, frame = cls.cap.read()

            if not ret:
                break  # 读取失败，跳出循环

            # 调用模型，检测当前帧
            results = cls.model(source=frame)

            # 提取置信度和类别信息
            for result in results:
                for box in result.boxes:
                    # 类别名称
                    class_name = result.names[int(box.cls.item())]
                    # 置信度
                    conf = round(box.conf.item(), 2)
                    # 坐标（左上角和右下角）
                    x_min, y_min, x_max, y_max = box.xyxy[0].tolist()

                    # 绘制检测结果：文字
                    cv2.putText(
                        frame,
                        f"{class_name} {conf}",
                        (int(x_min), int(y_min) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )
                    # 绘制检测结果：矩形框
                    cv2.rectangle(
                        frame,
                        (int(x_min), int(y_min)), (int(x_max), int(y_max)),
                        (0, 255, 0),
                        2
                    )

            # 绘制后的检测结果 -> 转为 jpg -> 通过字节流返回给客户端
            ret, buffer = cv2.imencode(".jpg", frame)
            # yield 返回
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

