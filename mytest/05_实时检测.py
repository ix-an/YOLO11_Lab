from ultralytics import YOLO
import cv2
"""
通过客户端操作：
    打开摄像头：进行检测
    关闭摄像头：关闭检测
"""

def detect():
    # 通过 opencv 的方法，打开摄像头
    cap = cv2.VideoCapture(0)
    # 加载模型
    model = YOLO("../weights/yolo11s.pt")
    # 监听检测到的内容
    while True:  # 死循环，必须给终止条件
        # 判断摄像头是否打开
        if not cap.isOpened():
            return
        # 摄像头打开了 --- ret 布尔值，否则读取到内容；frame 读取到的内容
        ret, frame = cap.read()
        # 判断内容是否为空
        if not ret:
            break
        # 读取到内容 --- 调用模型检测
        results = model(source=frame)
        # 提取置信度和类别信息
        for result in results:
            for box in result.boxes:
                # 类别名称
                class_name = result.names[int(box.cls.item())]
                print(class_name)
                # 置信度
                conf = round(box.conf.item(), 2)
                # 坐标（左上角和右下角）
                x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                # 绘制检测结果 --- putText【图像上绘制文本】、rectangle【绘制矩形框】
                cv2.putText(frame,
                            f"{class_name} {conf}",
                            (int(x_min), int(y_min - 5)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0),
                            1
                            )
                cv2.rectangle(frame,
                              (int(x_min), int(y_min)),
                              (int(x_max), int(y_max)),
                              (0, 255, 0),
                              2
                              )
        # 显示检测结果
        cv2.imshow("detect", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    detect()
