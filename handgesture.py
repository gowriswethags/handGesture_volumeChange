from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volumeInformation = volume.GetVolumeRange()
minVolume = volumeInformation[0]
maxVolume = volumeInformation[1]




import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
   status, img = cap.read()
   imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
   results = hands.process(imgRGB)
   multiLandMark = results.multi_hand_landmarks
   print(multiLandMark)
   if multiLandMark:
      indexPoint = ()
      thumbPoint = ()
      for handLms in multiLandMark:
         mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

         for idx, lm in enumerate(handLms.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            #print(idx, cx,cy)
            if idx == 4:
               thumbPoint = (cx, cy)
            if idx == 8:
               indexPoint = (cx, cy)

      cv2.circle(img, indexPoint, 15, (255, 255, 0), cv2.FILLED)
      cv2.circle(img, thumbPoint, 15, (255, 255, 0), cv2.FILLED)   
      cv2.line(img, indexPoint, thumbPoint, (255, 255, 0), 3)

      length = math.sqrt(((indexPoint[0]-thumbPoint[0]) **2)+ ((indexPoint[1]-thumbPoint[1]) **2))
      print(length)

      vol = np.interp(length, [6,216], [minVolume, maxVolume])
      print(vol)

      volume.SetMasterVolumeLevel(vol, None)

  
   cv2.imshow("HandGesture", img)
   cv2.waitKey(1)
