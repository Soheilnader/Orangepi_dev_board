import cv2
import numpy as np
import os

cap = cv2.VideoCapture("http://192.168.1.184:81/stream")
os.system("gpio mode 22 out")
os.system("gpio mode 23 out")
os.system("gpio mode 25 out")

while(True):
    ret, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height,width, _ = frame.shape
    

    cx = int(width / 2)
    cy = int(height / 2)


    #PICK PIXEL VALUE
    pixel_center = hsv_frame[cy,cx]
    hue_value = pixel_center[0]

    color = "Underfined"
    if hue_value < 5:
        color = "RED"
        os.system("gpio write 22 0")
        os.system("gpio write 23 0")
        os.system("gpio write 25 1")
    elif hue_value < 22:
        color = "ORANGE"
        os.system("gpio write 22 0")
        os.system("gpio write 23 0")
        os.system("gpio write 25 0")
    elif hue_value < 33:
        color = "YELLOW"
        os.system("gpio write 22 0")
        os.system("gpio write 23 0")
        os.system("gpio write 25 0")
    elif hue_value < 78:
        color = "GREEN" 
        os.system("gpio write 22 0")
        os.system("gpio write 23 1")
        os.system("gpio write 25 0")  
    elif hue_value < 131:
        color = "BLUE"
        os.system("gpio write 22 1")
        os.system("gpio write 23 0")
        os.system("gpio write 25 0")
    elif hue_value < 178:
        color = "VIOLET" 
        os.system("gpio write 22 0")
        os.system("gpio write 23 0")
        os.system("gpio write 25 0")
    else:
        color ="RED" 
        os.system("gpio write 22 0")
        os.system("gpio write 23 0")
        os.system("gpio write 25 1") 


    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
    cv2.putText(frame, color, (10,50), 0, 1.5, (b, g, r), 2)
    cv2.circle(frame, (cx, cy) , 5, (25, 25, 25), 3)


    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        os.system("gpio write 22 0")
        os.system("gpio write 23 0")
        os.system("gpio write 25 0")
        break

cap.release()
cv2.destroyAllWindows()

