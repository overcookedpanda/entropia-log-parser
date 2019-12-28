#!/usr/bin/env python3

import re
import numpy as nm
import pytesseract as ts
import cv2
from PIL import ImageGrab


def get_loot_values():
    ts.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    config = '-l eng --oem 1 --psm 4'
    while True:
        cap = ImageGrab.grab(bbox=captureBox)
        tesstr = ts.image_to_string(
            cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY), config=config
        )
        if re.search(r'(\w+.*)\b\s\((\d+.\d\d)\sPED\)', tesstr) is not None:
            f = open(r'C:\Users\ocpanda\Desktop\eu\eu2.log', 'a+')
            f.write(tesstr + '\n')
            f.close()
            # print(tesstr)
            line = tesstr.split("\n")
            for item in line:
                if re.search(r'(\w+.*)\b\s\((\d+.\d\d)\sPED\)', item) is not None:
                    item = re.sub(r',', '.', item)
                    print(item)


# Define capture window coordinates:
# (left_x, top_y, right_x, bottom_y)

captureBox = (76, 50, 435, 350)
get_loot_values()
