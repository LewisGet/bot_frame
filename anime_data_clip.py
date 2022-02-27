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

            """
            img_hsv = img_s[:]
            img_hsv = cv2.cvtColor(img_hsv, cv2.COLOR_RGB2HSV)
            img_r, img_g, img_b = [img_hsv[:]] * 3

            img_r = cv2.inRange(img_r, np.array([50, 0, 0]), np.array([255, 200, 255]))
            img_g = cv2.inRange(img_g, np.array([0, 50, 0]), np.array([200, 255, 200]))
            img_b = cv2.inRange(img_b, np.array([0, 0, 50]), np.array([200, 200, 255]))

            img_r = cv2.bitwise_and(img_s, img_s, mask=img_r)
            img_g = cv2.bitwise_and(img_s, img_s, mask=img_g)
            img_b = cv2.bitwise_and(img_s, img_s, mask=img_b)

            img_r = cv2.cvtColor(img_r, cv2.COLOR_RGB2GRAY)
            img_g = cv2.cvtColor(img_g, cv2.COLOR_RGB2GRAY)
            img_b = cv2.cvtColor(img_b, cv2.COLOR_RGB2GRAY)
            img_s = cv2.cvtColor(img_s, cv2.COLOR_RGB2GRAY)

            view_image = np.concatenate((img_s, img_r, img_g, img_b), axis=0)
            """
            view_image = img_s[:]

            if i == 0:
                mouse.hook(mouse_events.append)
                keyboard.start_recording()
                images_to_save = view_image[:]
            else:
                images_to_save = np.concatenate((images_to_save, view_image), axis=1)

            if i == 2:
                mouse.unhook(mouse_events.append)
                keyboard_events = keyboard.stop_recording()

                labels = [unit.mouse_event_process(mouse_events[-30:]), unit.keyboard_event_process(keyboard_events[-30:])]
                xs.append(images_to_save)
                ys.append(labels)
                cv2.imshow("save", images_to_save)
                print(labels, "\n")

                i = 0

                if cv2.waitKey(25) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    np.save(config.save_dataset_content, xs)
                    np.save(config.save_dataset_label, ys)
                    break
            else:
                i += 1



