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
import platform

def draw_lines(image):
    # top line
    cv2.line(image,
             (0,int(len(image)/4)),
             (len(image[0]),int(len(image)/4)),
             (255,0,0), 1)
    # bottom line
    cv2.line(image,
             (0,int(len(image)-len(image)/4)),
             (len(image[0]),int(len(image)-len(image)/4)),
             (255,0,0), 1)
    # left line
    cv2.line(image,
             (int(len(image[0])/4),0),
             (int(len(image[0])/4),len(image)),
             (255,0,0), 1)
    # right line
    cv2.line(image,
             (int(len(image[0])-len(image[0])/4),0),
             (int(len(image[0])-len(image[0])/4),len(image)),
             (255,0,0), 1)
    
def cursor_click(eyes, eye_x_cord, roi_width):
    cursor_x, cursor_y = pag.position()
    if(eye_x_cord >= roi_width/2):
        pag.click(cursor_x, cursor_y)
        #print('Left Click!')
    else:
        pag.click(cursor_x, cursor_y, button='right')
        #print('Right Click!')
    
def cursor_move(image, x_coord, y_coord, width, height, distance=5):
    if (x_coord < int(len(image[0])/4) 
            and y_coord < int(len(image)/4)):
        pag.moveRel(-1*distance, -1*distance)
        #print('left and up')
        
    elif (x_coord + width > int(len(image[0])-len(image[0])/4) 
            and y_coord < int(len(image)/4)):
        pag.moveRel(distance, -1*distance)  
        #print('right and up')
        
    elif (x_coord < int(len(image[0])/4) 
            and y_coord + height > int(len(image)-len(image)/4)):
        pag.moveRel(-1*distance, distance)     
        #print('left and down')
        
    elif (x_coord + width > int(len(image[0])-len(image[0])/4) 
            and y_coord + height > int(len(image)-len(image)/4)):
        pag.moveRel(distance, distance)
        #print('right and down') 
        
    elif (x_coord < int(len(image[0])/4)):
        pag.moveRel(-1*distance, 0)   
        #print('left')
        
    elif (x_coord + width > int(len(image[0])-len(image[0])/4)):
        pag.moveRel(distance, 0)     
        #print('right')
        
    elif (y_coord < int(len(image)/4)):  
        pag.moveRel(0, -1*distance)
        #print('up') 
        
    elif (y_coord + height > int(len(image)-len(image)/4)):
        pag.moveRel(0, distance)
        #print('down')


        
if __name__ == '__main__':        
    # uploading classifiers
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades 
                                        + 'haarcascade_frontalface_default.xml')
    eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades 
                                       + 'haarcascade_eye.xml')
    
    #setting refreshing time for cursor movement, 
    #read the monitor resolution to put cursor at the center of screen
    pag.PAUSE = 0.01
    scrx, scry = pag.size()
    pag.moveTo(scrx/2, scry/2)
    
    cap = cv2.VideoCapture(0)
    
    while (True):
        _, frame = cap.read()
    
        if platform.system() == 'Linux':
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
                cv2.rectangle(roi_color, 
                              (ex, ey), 
                              (ex + ew, ey + eh), 
                              (0, 0, 255), 1)
                #print(x, w, ex, ew)
    
            if len(eyes) == 1:
                cursor_click(eyes, ex, w)
                
            else:
                cursor_move(frame, x, y, w, h)
    
        draw_lines(frame)
    
        cv2.imshow('Captured camera video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
