import unit
import config
import numpy as np
import cv2
import mss
import time
import os


if __name__ == '__main__':
    try:
        xs, ys = np.load(config.save_dataset_content), np.load(config.save_dataset_label)
        xs, ys = xs.tolist(), ys.tolist()
    except:
        xs, ys = [], []

    # debug
    time.sleep(5)

    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {
            "top": config.recorder["start"]["y"],
            "left": config.recorder["start"]["x"],
            "width": config.recorder["base_size"]["x"],
            "height": config.recorder["base_size"]["y"]
        }

        while "Screen capturing":
            images_to_view = []
            images_to_save = []

            for i in range(3):
                img = np.array(sct.grab(monitor))
                img_b, img_s = img[:], img[:]

                img_b = cv2.resize(img_b, (1920, 1080))
                img_s = cv2.resize(img_s, (int(config.recorder["base_size"]["x"] / 2), int(config.recorder["base_size"]["y"] / 2)))
                img_s = cv2.cvtColor(img_s, cv2.COLOR_RGBA2GRAY)

                cv2.imshow("display_b %d" % i, img_b)
                cv2.imshow("display %d" % i, img_s)

                images_to_view.extend(img_b.tolist())

                if i == 0:
                    images_to_save = img_s
                else:
                    images_to_save = np.concatenate((images_to_save, img_s), axis=1)

            print(np.array(images_to_save).shape)

            cv2.imshow("save", images_to_save)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                label = int(input("label %s : \n" % str(list(enumerate(config.labels)))))
                cv2.destroyAllWindows()
                xs.append(images_to_save)
                ys.append(label)

                np.save(config.save_dataset_content, xs)
                np.save(config.save_dataset_label, ys)
                break
