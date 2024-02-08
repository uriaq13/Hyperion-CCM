import numpy as np

from djitellopy import tello

import cv2


drone = tello.Tello()

drone.connect()

print(drone.get_battery())

drone.streamon()

is_flying = False

drone.set_speed(15)


def empty():
    pass


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 320, 240)
cv2.createTrackbar("Threshold1", "Parameters", 23, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 20, 255, empty)
cv2.createTrackbar("Area", "Parameters", 5000, 10000, empty)



def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img, imgContour):
    approx = []
    
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255,0,255),7)
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            print(len(approx))
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
            
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            
    return approx
            
 
def DetectCircle(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circle = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=200, maxRadius=300)
    
    if circle is not None:
        circle = np.uint16(np.around(circle))
        for i in circle[0, :]:
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
            
    return circle
    
    
#Rigth Forward Function
def RF():
    #rigth
    drone.move_right(20)
    #Forward
    drone.move_forward(80)
    #Rotate
    drone.rotate_counter_clockwise(90)
    #Move for next
    drone.move_right(30)
    drone.move_forward(50)
    
    
#Up and forward    
def UF():
    #Rigth
    drone.move_right(40)
    #Up
    drone.move_up(20)
    #Forward
    drone.move_forward(40)
    drone.rotate_clockwise(90)
    #Move
    drone.move_left(30)
    drone.move_forward(50)

#Down Forward
def DF():
    #Rigth
    drone.move_right(50)
    #Down
    drone.move_down(30)
    #Forward
    drone.move_forward(120)
    drone.rotate_counter_clockwise(90)
    #Move
    drone.move_right(30)
    drone.move_forward(70)


#LeftForward
def LF():
    #rigth
    drone.move_right(100)
    #Forward
    drone.move_forward(120)
    #Rotate
    drone.rotate_counter_clockwise(90)
    #Move for next
    drone.move_forward(80)
    
    

key = cv2.waitKey(1) & 0xFF

while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (480, 360))
    imgContour = img.copy()

    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    approx = getContours(imgDil, imgContour)
    figure = len(approx)

    imgStack = stackImages(0.8, ([img, imgGray, imgCanny],
                                 [imgDil, imgContour, imgContour]))

    cv2.imshow("Result", imgStack)

    if key == ord('t'):
        drone.takeoff()
        drone.move_up(75)
        drone.move_forward(50)
        
        a= 3
        b = 4
        c = 6
        #dc +{'a':DF(),'b':LF()...}
        #if figure in dc:
        #   dc[figure]
        
        if figure == a:
            print("triangulo")
            DF()
        elif figure == b:
            print("Cuadrado")
            LF()
        elif figure == c:
            print("Hexagono")
            UF()
        else:
            print("Circle")
            DF()

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

drone.land()
drone.streamoff()
cv2.destroyAllWindows()
