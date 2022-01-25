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
