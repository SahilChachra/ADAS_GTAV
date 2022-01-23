import numpy as np
import cv2
import time
from directKeys import PressKey, W, A, S, D, ReleaseKey
import math
import warnings
warnings.filterwarnings("ignore")

from PIL import ImageGrab
import win32gui, win32ui, win32con, win32api

import torch

########### CONTROLS START################
def go_straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    time.sleep(0.5)
    ReleaseKey(W)

def turn_left():
    PressKey(A)
    PressKey(W)
    time.sleep(0.5)
    ReleaseKey(A)

def turn_right():
    PressKey(D)
    ReleaseKey(A)
    time.sleep(0.5)
    ReleaseKey(D)

def slow_down():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    PressKey(S)
    time.sleep(0.5)
    ReleaseKey(S)

################### CONTROL ENDS #####################

################### SCREEN CAPTURE ###################

def grab_screen(region=None):
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

######################################################

##################### PROCESSING #####################

def process_img(image, model):
    try:
        output = model(image)
        op = output.pandas().xyxy[0]
        for index, row in op.iterrows():
            if row["confidence"] > 0.75:
                xmin = int(row["xmin"])
                ymin = int(row["ymin"])
                xmax = int(row["xmax"])
                ymax = int(row["ymax"])
                name = row["name"]

                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

                mid_object_x, mid_object_y = (xmin + xmax)//2, (ymin + ymax)//2
                cv2.circle(image, (mid_object_x, mid_object_y), 5, (255,0,0), -1)
                cv2.line(image, (0, 550), (800, 550), (120, 150, 90), 3)

                mid_line_x, mid_line_y = 400, 550
                # angle = math.degrees(math.atan2(mid_object_y - mid_line_y, mid_object_x - mid_line_x))
                # print('Angle is :',angle)
                dist = math.dist([mid_object_x, mid_object_y], [mid_line_x, mid_line_y])
                # print("Distance is :", dist)

                cv2.line(image, (400, 550), (mid_object_x, mid_object_y), (90, 190, 200), 2)
                # cv2.putText(image, str(dist), ((mid_object_x - 400)//2, (mid_object_y - 550)//2), cv2.FONT_HERSHEY_SIMPLEX, 5, (120, 155, 50), 2)
                cv2.putText(image, name + f',{int(dist)}', (xmin - 10, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                if dist < 150 and name.lower() in ['car', 'perso', 'truck']:
                    slow_down()
                    print("Slowing down...")

        return image
    except TypeError:
        pass


def main():
    prev_time = 0
    print("Staring in ...")
    for i in range(4)[::-1]:
        print(i+1)
        time.sleep(1)
    try:
        model = torch.hub.load("ultralytics/yolov5", "yolov5s")
        model.cuda()
    except exception as e:
        print("While loading model, exception occured.\n", e)

    while True:
        #screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 600)))
        screen = grab_screen(region=(0, 0, 799, 599))

        curr_time = time.time()
        print("FPS : {0}".format(1 // (curr_time - prev_time)))
        prev_time = curr_time

        #processedImg = process_img(screen)
        processedImg = process_img(screen, model)

        #cv2.imshow("GTA V", processedImg)
        cv2.imshow("GTA V", cv2.cvtColor(processedImg, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('k'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()
