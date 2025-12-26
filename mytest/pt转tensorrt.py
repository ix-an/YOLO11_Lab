from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("../../yolo11/yolo11s.pt")
    # engine就是 tensorrt格式的后缀
    model.export(
        format="engine",
        data="./datasets/african-wildlife.yaml",
        int8=True,
        dynamic=True,
    )