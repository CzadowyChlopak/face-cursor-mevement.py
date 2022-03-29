# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 14:10:14 2022

@author: Dominik Dmowski

General rules:
x,y -------> TOP LEFT FACE CORNER
x1,y1 -------> BOTTOM RIGHT FACE CORNER

1) X < Xl ----> LEFT
2) X1 > Xp ----> RIGHT
3) Y < Yg ----> UP
4) Y1 >Yd ----> DOWN
"""

import cv2
import pyautogui as pag

# uploading classifiers
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

#setting refreshing time for cursor movement, read the monitor resolution to put cursor at the center of screen
pag.PAUSE = 0.01
scrx, scry = pag.size()
pag.moveTo(scrx/2, scry/2)

cap = cv2.VideoCapture(0)

while (True):
    _, frame = cap.read()

    cv2.flip(frame, 1, frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=3,
                                         minSize=(60,60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 1)
        roi_gray = gray[y:y+h, x:x+w,]
        roi_color = frame[y:y+h, x:x+w,]
        eyes = eyeCascade.detectMultiScale(roi_gray,
                                             scaleFactor=1.1,
                                             minNeighbors=3,
                                             minSize=(20,20),
                                             flags=cv2.CASCADE_SCALE_IMAGE)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 1)

        if len(eyes) == 1:
            curx, cury = pag.position()
            pag.click(curx, cury, )
            #print('Click!')
        else:
            if (x < int(len(frame[0])/4) and y < int(len(frame)/4)):
                #print('left and up')
                pag.moveRel(-5, -5)
            elif (x+w > int(len(frame[0])-len(frame[0])/4) and y < int(len(frame)/4)):
                #print('right and up')
                pag.moveRel(5, -5)
            elif (x < int(len(frame[0])/4) and y+h > int(len(frame)-len(frame)/4)):
                #print('left and down')
                pag.moveRel(-5, 5)
            elif (x+w > int(len(frame[0])-len(frame[0])/4) and y+h > int(len(frame)-len(frame)/4)):
                #print('right and down')
                pag.moveRel(5, 5)
            elif (x < int(len(frame[0])/4)):
                #print('left')
                pag.moveRel(-5, 0)
            elif (x+w > int(len(frame[0])-len(frame[0])/4)):
                #print('right')
                pag.moveRel(5, 0)
            elif (y < int(len(frame)/4)):
                #print('up')
                pag.moveRel(0, -5)
            elif (y+h > int(len(frame)-len(frame)/4)):
                #print('down')
                pag.moveRel(0, 5)

    # checking the camera resolution
    #print(len(frame),len(frame[0]))

    # top line
    cv2.line(frame,
             (0,int(len(frame)/4)),
             (len(frame[0]),int(len(frame)/4)),
             (255,0,0), 1)
    # bottom line
    cv2.line(frame,
             (0,int(len(frame)-len(frame)/4)),
             (len(frame[0]),int(len(frame)-len(frame)/4)),
             (255,0,0), 1)
    # left line
    cv2.line(frame,
             (int(len(frame[0])/4),0),
             (int(len(frame[0])/4),len(frame)),
             (255,0,0), 1)
    # right line
    cv2.line(frame,
             (int(len(frame[0])-len(frame[0])/4),0),
             (int(len(frame[0])-len(frame[0])/4),len(frame)),
             (255,0,0), 1)



    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()