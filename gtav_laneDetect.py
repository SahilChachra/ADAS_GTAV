import numpy as np
import cv2
import time
from directKeys import PressKey, W, A, S, D, ReleaseKey
import warnings

warnings.filterwarnings("ignore")
from PIL import ImageGrab
import win32gui, win32ui, win32con, win32api


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


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, threshold1=150, threshold2=250)
    return canny


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            if line is not None:
                x1, y1, x2, y2 = line.reshape(4)
                try:
                    cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
                except:
                    pass

    return line_image


def roi(image):
    # replace object in np.array(<object>)
    # full res [[(100,900),(1600,700),(700,250)]]
    # windowed np.array([[(200, 420), (900, 400), (500, 30)]])
    # first-person [[(10, 635), (10, 400), (430, 290), (800, 400), (800, 635)]]
    # polygons = np.array([[(10, 635), (10, 400), (430, 290), (800, 400), (800, 635)]])
    # polygons = np.array([[[5, 600], [5, 520], [300, 250], [400, 250], [100, 575],
    #        [650, 575], [400, 250], [500, 250], [800, 520], [800, 600]]], np.int32)
    polygons = np.array([[(0, 600), (0, 400), (275, 275), (360, 275), (225, 575), (545, 575),
                          (400, 275), (490, 275), (800, 400), (800, 600)]])

    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked = cv2.bitwise_and(image, mask)
    return masked


def return_coordinates(image, lines):
    try:
        slope, intercept = lines
        y1 = image.shape[0]
        y2 = int(y1 * 3 / 5)
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        return np.array([x1, y1, x2, y2])
    except Exception as e:
        print("Exception in 'return_coordinates' :", e)
        pass


def average_slope_intercept(image, lines):
    left_lines = []
    right_lines = []
    try:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            coordinates = np.polyfit((x1, x2), (y1, y2), 1)
            slope = coordinates[0]
            intercept = coordinates[1]
            # print('Slope {0}, Intercept {1}'.format(slope, intercept))
            if slope > 0:
                right_lines.append((slope, intercept))
            else:
                left_lines.append((slope, intercept))

        left_lines_avg = np.average(left_lines, axis=0)
        right_lines_avg = np.average(right_lines, axis=0)
        left_line = return_coordinates(image, left_lines_avg)
        right_line = return_coordinates(image, right_lines_avg)
        try:
            return np.array([left_line, right_line])
        except Exception as e:
            pass
    except Exception as e:
        pass


def process_img(image):
    try:
        input_image = np.copy(image)
        canny_image = canny(input_image)
        cropped_image = roi(canny_image)
        lines = cv2.HoughLinesP(cropped_image, cv2.HOUGH_PROBABILISTIC,
                                np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
        average_lines = average_slope_intercept(input_image, lines)
        try:
            lx1, ly1, lx2, ly2 = average_lines[0]
            rx1, ry1, rx2, ry2 = average_lines[1]
            l_slope = (lx2 - lx1) / (ly2 - ly1)
            r_slope = (rx2 - rx1) / (ry2 - ry1)
            print('Left slope :', l_slope)
            print('Right slope :', r_slope)
        except:
            l_slope = -1.2
            r_slope = 1.23
        # exit(0)
        line_image = display_lines(input_image, average_lines)
        combined_image = cv2.addWeighted(input_image, 0.7, line_image, 1, 1)
        return combined_image, l_slope, r_slope, cropped_image
    except TypeError:
        pass


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


def main():
    prev_time = 0
    print("Staring in ...")
    for i in range(4)[::-1]:
        print(i + 1)
        time.sleep(1)

    while True:
        # screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 600)))
        screen = grab_screen(region=(0, 0, 820, 620))

        curr_time = time.time()
        print("FPS : {0}".format(1 // (curr_time - prev_time)))
        prev_time = curr_time

        processedImg, l_slope, r_slope, roi = process_img(screen)

        if -2 < l_slope < -1.7:
            turn_left()
            print("Going left...")
        elif r_slope > 1.7 and r_slope < 2.3:
            turn_right()
            print("Going right...")
        elif l_slope >= -1.7 and r_slope <= 1.7:
            go_straight()
            print("Going straight...")
        else:
            slow_down()

        cv2.imshow("GTA V", cv2.cvtColor(processedImg, cv2.COLOR_BGR2RGB))
        cv2.imshow("GTA V ROI", roi)

        if cv2.waitKey(25) & 0xFF == ord('k'):
            cv2.destroyAllWindows()
            break


main()

# 1. Edit fetching screen thing - Done
# 2. Have default lanes
# 3. Fix overlapping of lanes
