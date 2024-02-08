import cv2
import numpy as np
 
img = cv2.imread("C:/Users/alber/OneDrive - Instituto Tecnologico y de Estudios Superiores de Monterrey/Hyperion/Programas/Drones2024/Resources/lambo.png")
print(img.shape)

imgResize = cv2.resize(img, (1000, 500))
print(imgResize.shape)

imgCropped = img[0:200, 200:500]

cv2.imshow("Lambo", img)
cv2.imshow("Lambo Resize", imgResize)
cv2.imshow("Lambo Cropped", imgCropped)

cv2.waitKey(0)