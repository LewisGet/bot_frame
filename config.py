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

labels = ["none", "up", "down", "left", "right", "up and left", "up and right", "down and left", "down and right"]
# 圖片縮小一半三偵影格橫放
input_size = 600, 150
save_model_path = os.path.join(".", "ckpt", "alexnet")
save_dataset_base_path = os.path.join(".", "dataset")
save_dataset_content = os.path.join(save_dataset_base_path, "x.npy")
save_dataset_label = os.path.join(save_dataset_base_path, "y.npy")
