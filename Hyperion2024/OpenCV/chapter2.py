import cv2
import numpy as np

img = cv2.imread("C:/Users/alber/OneDrive - Instituto Tecnologico y de Estudios Superiores de Monterrey/Hyperion/Programas/Drones2024/Resources/lena.png")
kernel = np.ones((5,5),np.uint8)

Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
Blur = cv2.GaussianBlur(Gray,(7,7),0)
Canny = cv2.Canny(img, 150, 200)
Dialation = cv2.dilate(Canny, kernel,iterations=1)
Eroded = cv2.erode(Dialation, kernel, iterations=1)

cv2.imshow("Gray", Gray)
cv2.imshow("Blur", Blur)
cv2.imshow("Canny", Canny)
cv2.imshow("Dialation", Dialation)
cv2.imshow("Eroded", Eroded)
cv2.waitKey(0)