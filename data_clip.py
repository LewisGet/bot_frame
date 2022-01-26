import unit
import config
import numpy as np
import cv2
import mss
import time
import os


def images_pre_save_resize(images):
    for i in range(3):
        img = cv2.resize(images[i], (int(config.recorder["base_size"]["x"] / 2), int(config.recorder["base_size"]["y"] / 2)))
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

        if i == 0:
            return_image = img
        else:
            return_image = np.concatenate((return_image, img), axis=1)

    return return_image


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
            images = []

            for i in range(3):
                img = np.array(sct.grab(monitor))
                images.append(img)
                cv2.imshow("save % d" % i, img)

            images_to_save = images_pre_save_resize(images)
            cv2.imshow("save", images_to_save)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                label = [int(i) for i in list(input("label %s : \n" % str(list(enumerate(config.labels)))))]
                cv2.destroyAllWindows()
                xs.append(images_to_save)
                ys.append(label)

                np.save(config.save_dataset_content, xs)
                np.save(config.save_dataset_label, ys)
                break
