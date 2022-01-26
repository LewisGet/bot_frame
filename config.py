import os

recorder = {
    "prefix": {
        "x": 1920, "y": 0
    },
    "center": {
        "x": 960, "y": 540
    },
    "base_size": {
        "x": 400, "y": 300
    },
    "start": {
        "x": 0, "y": 0
    },
    "end": {
        "x": 0, "y": 0
    }
}

cx, cy = recorder["center"]["x"], recorder["center"]["y"]
bx, by = recorder["base_size"]["x"], recorder["base_size"]["y"]

recorder["start"]["x"], recorder["start"]["y"] = recorder["prefix"]["x"] + cx - int(bx / 2), recorder["prefix"]["y"] + cy - int(by / 2)
recorder["end"]["x"], recorder["end"]["y"] = recorder["prefix"]["x"] + cx + int(bx / 2), recorder["prefix"]["y"] + cy + int(by / 2)

# xy 距離圖片的 0, 0 使用二進至百分比 xy 距離，舉例： x 80% y 20%, x1010000, y 0010100
# 因為 100% 要站 7位元，所以我們改 10倍率 1 代表 10% 這樣一個數字只需要四個位元
labels = ["none", "x:---?", "x:--?-", "x:-?--", "x:?---", "y:---?", "y:--?-", "y:-?--", "y:?---"]
# 圖片縮小一半三偵影格橫放
input_size = 600, 150
save_model_path = os.path.join(".", "ckpt", "alexnet")
save_dataset_base_path = os.path.join(".", "dataset")
save_dataset_content = os.path.join(save_dataset_base_path, "x.npy")
save_dataset_label = os.path.join(save_dataset_base_path, "y.npy")
