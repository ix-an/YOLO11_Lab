from ultralytics import YOLO
from my_server.settings import BASE_DIR
import os



if __name__ == '__main__':

    # 加载模型
    model = YOLO(os.path.join(BASE_DIR, "weights", "yolo11s.engine"))
    classes_number = {name: 0 for name in model.names.values()}
    filename = "01.jpg"
    source = os.path.join(BASE_DIR, "mytest", filename)
    # 自定义保存目录（默认保存在 runs/detect/predict? 目录下）
    project = os.path.join(BASE_DIR, "runs", "detect")
    results = model.predict(source=source, save=True, project=project)

    result_url = ""
    total_conf = 0.0
    length = 0

    for res in results:
        url = res.save_dir.split("detect")[-1].replace("\\", "")
        # 预测结果数量
        length = len(res.boxes)
        for box in res.boxes:
            # 获取类别名称
            class_name = res.names[int(box.cls.item())]
            # 类别计数
            classes_number[class_name] += 1
            # 获取置信度（取平均值）
            total_conf += round(box.conf.item(), 2)

    # 过滤出值非 0的类别
    non_zero_classes = {k: v for k, v in classes_number.items() if v != 0}
    # 结果保存路径
    result_url = "runs/detect/" + url + "/" + filename

    print("检测到的类别及数量：", non_zero_classes)
    if length > 0:
        print("平均置信度：", round(total_conf / length, 2))
    else:
        print("无检测结果，平均置信度为 0")
    print("结果保存路径：", result_url)



