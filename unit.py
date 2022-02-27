import numpy as np
import cv2
import mss
import os
import win32api
import win32con
import ctypes
import time
import config
import mouse
import keyboard


SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def mouse_event_process(datasets):
    left_click, right_click = 0, 0
    x, y = 0, 0

    for data in datasets:
        if type(data) is mouse._mouse_event.MoveEvent:
            x, y = data.x, data.y
        elif type(data) is mouse._mouse_event.ButtonEvent:
            if data.event_type == "down":
                if data.button == "left":
                    left_click = 1
                elif data.button == "right":
                    right_click = 1
            elif data.event_type == "up":
                if data.button == "left":
                    left_click = -1
                elif data.button == "right":
                    right_click = -1

    return [x, y, left_click, right_click]

def keyboard_event_process(datasets):
    def key_register():
        w, a, s, d, space, e, r, q, z, ctrl = [0] * 10
        return locals()

    keys = key_register()
    move_x, move_y = 0, 0

    for data in datasets:
        for i, v in enumerate(keys):
            if data.event_type == "down":
                value = 1
            elif data.event_type == "up":
                value = -1

            if v == data.name:
                keys[v] = value

    if keys["w"] > 0:
        move_y = 1

    if keys["s"] > 0:
        move_y = -1

    if keys["d"] > 0:
        move_x = 1

    if keys["a"] > 0:
        move_x = -1

    keys['move_x'] = move_x
    keys['move_y'] = move_y

    return keys


class Mouse:
    @staticmethod
    def move_relative(x, y):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))
        cmd = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(cmd), ctypes.sizeof(cmd))

    @staticmethod
    def get_position():
        return win32api.GetCursorPos()


if __name__ == '__main__':
    # debug
    time.sleep(5)

    move_series = [
        [-1, 0],
        [1, 0],
        [0, -1],
        [0, 1],
        [-1, -1],
        [1, 1],
        [1, 1],
        [-1, -1]
    ]

    move_index = 0

    m = Mouse()

    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {
            "top": config.recorder["start"]["y"],
            "left": config.recorder["start"]["x"],
            "width": config.recorder["base_size"]["x"],
            "height": config.recorder["base_size"]["y"]
        }

        while "Screen capturing":
            # Get raw pixels from the screen, save it to a Numpy array
            img = np.array(sct.grab(monitor))

            print(img.shape)
            print(Mouse.get_position())

            m.move_relative(*move_series[move_index])
            move_index += 1
            if move_index >= len(move_series):
                move_index = 0

            img = cv2.resize(img, (1920, 1080))
            cv2.imshow("zoom", img)
            time.sleep(1)

            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

    # with mss.mss() as sct:
    #     # Part of the screen to capture
    #     monitor = {
    #         "top": config.recorder["prefix"]["y"],
    #         "left": config.recorder["prefix"]["x"],
    #         "width": 1920,
    #         "height": 1080
    #     }
    #
    #     while "Screen capturing":
    #         img = np.array(sct.grab(monitor))
    #
    #         x, y = Mouse.get_position()
    #         x, y = x - config.recorder["prefix"]["x"], y - config.recorder["prefix"]["y"]
    #
    #         img[y - 10:y + 10, x - 10:x + 10][:] = 0
    #
    #         img = cv2.resize(img, (1920, 1080))
    #         cv2.imshow("zoom", img)
    #
    #         # Press "q" to quit
    #         if cv2.waitKey(25) & 0xFF == ord("q"):
    #             cv2.destroyAllWindows()
    #             break
