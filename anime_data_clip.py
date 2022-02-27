import unit
import numpy as np
import cv2
import mss
import keyboard
import mouse
import time
import config

if __name__ == '__main__':
    try:
        xs, ys = np.load(config.save_dataset_content), np.load(config.save_dataset_label, allow_pickle=True)
        xs, ys = xs.tolist(), ys.tolist()
    except:
        xs, ys = [], []

    # debug

    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {
            "top": 0,
            "left": 1920,
            "width": 1920,
            "height": 1080
        }
        images_to_save = []
        mouse_events = []

        i = 0

        while "Screen capturing":
            img = np.array(sct.grab(monitor))
            img_s = cv2.resize(img[:], (480, 270))
            img_s = cv2.cvtColor(img_s, cv2.COLOR_RGBA2RGB)
            images_to_save = img_s[:]

            mouse.hook(mouse_events.append)
            keyboard.start_recording()

            time.sleep(0.01)

            mouse.unhook(mouse_events.append)
            keyboard_events = keyboard.stop_recording()

            labels = [unit.mouse_event_process(mouse_events[:]), unit.keyboard_event_process(keyboard_events[:])]
            xs.append(images_to_save)
            ys.append(labels)
            cv2.imshow("save", images_to_save)
            print(labels, "\n")

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                np.save(config.save_dataset_content, xs)
                np.save(config.save_dataset_label, ys)
                break



