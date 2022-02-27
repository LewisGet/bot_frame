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
        xs, ys = np.load(config.save_dataset_content), np.load(config.save_dataset_label)
        xs, ys = xs.tolist(), ys.tolist()
    except:
        xs, ys = [], []

    # debug

    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {
            "top": config.recorder["start"]["y"],
            "left": config.recorder["start"]["x"],
            "width": config.recorder["base_size"]["x"],
            "height": config.recorder["base_size"]["y"]
        }
        images_to_save = []
        mouse_events = []

        i = 0

        while "Screen capturing":
            img = np.array(sct.grab(monitor))
            img_s = cv2.cvtColor(img[:], cv2.COLOR_RGBA2RGB)
            images_to_save = img_s[:]

            mouse.hook(mouse_events.append)
            keyboard.start_recording()

            time.sleep(0.01)

            mouse.unhook(mouse_events.append)
            keyboard_events = keyboard.stop_recording()

            labels = [unit.mouse_event_process(mouse_events[-30:]), unit.keyboard_event_process(keyboard_events[-30:])]

            if labels[0][3] == 1:
	            xs.append(images_to_save)
	            ys.append(labels)
	            print(labels, "\n")

            cv2.imshow("save", images_to_save)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                np.save(config.save_dataset_content, xs)
                np.save(config.save_dataset_label, ys)
                break


