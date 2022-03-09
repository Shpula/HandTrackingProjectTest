import cv2
import time
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
timer = 3
detector = htm.handDetector(detectionCon=0.9)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1b, y1b = lmList[20][1], lmList[20][2]
        x2b, y2b = lmList[4][1], lmList[4][2]
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cxb, cyb = (x1b + x2b) // 2, (y1b + y2b) // 2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = math.hypot(x2 - x1, y2 - y1)
        lengthB = math.hypot(x2b - x1b, y2b - y1b)

        cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 1)
        cv2.putText(img, f'{round(length)}', (cx+30, cy+10), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 255), 3)
        print(int(length))
        #volume.SetMasterVolumeLevel(length, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        if lengthB < 30:
            timer -= 1 / 15
            cv2.circle(img, (cxb, cyb), 10, (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'Exit in {round(timer)} second', (cxb, cyb), cv2.FONT_HERSHEY_COMPLEX,
                        0.7, (0, 0, 0), 3)
            if round(timer) == -1:
                break
        else:
            timer = 3

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
