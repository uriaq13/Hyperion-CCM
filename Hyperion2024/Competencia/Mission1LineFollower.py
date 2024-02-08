import numpy as np

from djitellopy import tello

import cv2

drone = tello.Tello()

drone.connect()

print(drone.get_battery())

drone.streamon()


hsvVals = [80,0,0,145,255,255]

sensors = 3

threshold = 0.2

width, height = 480, 360

senstivity = 3  

weights = [-25, -15, 0, 15, 25]

fSpeed = 10

curve = 0

is_flying = False

def thresholding(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([hsvVals[0], hsvVals[1], hsvVals[2]])

    upper = np.array([hsvVals[3], hsvVals[4], hsvVals[5]])

    mask = cv2.inRange(hsv, lower, upper)

    return mask

def getContours(imgThres, img):

    cx = 0

    contours, hieracrhy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:

        biggest = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(biggest)

        cx = x + w // 2

        cy = y + h // 2

        cv2.drawContours(img, biggest, -1, (255, 0, 255), 7)

        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    return cx

def getSensorOutput(imgThres, sensors):

    imgs = np.hsplit(imgThres, sensors)

    totalPixels = (img.shape[1] // sensors) * img.shape[0]

    senOut = []

    for x, im in enumerate(imgs):

        pixelCount = cv2.countNonZero(im)

        if pixelCount > threshold * totalPixels:

            senOut.append(1)

        else:

            senOut.append(0)

        

    return senOut

def sendCommands(senOut, cx):

    global curve

    ## TRANSLATION

    lr = (cx - width // 2) // senstivity

    lr = int(np.clip(lr, -10, 10))

    if 2 > lr > -2: lr = 0

    ## Rotation

    if   senOut == [1, 0, 0]: curve = weights[0]

    elif senOut == [1, 1, 0]: curve = weights[1]

    elif senOut == [0, 1, 0]: curve = weights[2]

    elif senOut == [0, 1, 1]: curve = weights[3]

    elif senOut == [0, 0, 1]: curve = weights[4]

    elif senOut == [0, 0, 0]: curve = weights[2]

    elif senOut == [1, 1, 1]: curve = weights[2]

    elif senOut == [1, 0, 1]: curve = weights[2]

    drone.send_rc_control(lr, fSpeed, 0, curve)
    
    
# def Circle(img):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.medianBlur(gray, 5)
#     circle = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=200, maxRadius=300)
    
#     if circle is not None:
#         circle = np.uint16(np.around(circle))
#         for i in circle[0, :]:
#             cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
#             cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
            
#     return circle
    

while True:


    img = drone.get_frame_read().frame

    img = cv2.resize(img, (width, height))

    img = cv2.flip(img, 0)

    imgThres = thresholding(img)

    cx = getContours(imgThres, img)  ## For Translation

    senOut = getSensorOutput(imgThres, sensors)  ## Rotation

    sendCommands(senOut, cx)
    
    
    if is_flying:
        cv2.putText(img,"Drone is Flying", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    else:
        cv2.putText(img,"Drone is not Flying", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Output", img)

    cv2.imshow("Path", imgThres)

    key = cv2.waitKey(1)&0xFF
        
    if key==ord('q'):
        drone.land()
        drone.streamoff()
        break
    elif key ==ord('t'):
        if is_flying:
            drone.land()
        else:
            drone.takeoff()
        is_flying = not is_flying
        
cv2.destroyAllWindows()
    
        