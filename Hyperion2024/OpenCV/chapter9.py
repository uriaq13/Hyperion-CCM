import cv2

faceCascade = cv2.CascadeClassifier("C:/Users/alber/OneDrive - Instituto Tecnologico y de Estudios Superiores de Monterrey/Hyperion/Programas/Drones2024/Resources/haarcascades/haarcascades/haarcascade_frontalface_default.xml")
img = cv2.imread("C:/Users/alber/OneDrive - Instituto Tecnologico y de Estudios Superiores de Monterrey/Hyperion/Programas/Drones2024/Resources/lena.png")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img,(x, y), (x + w, y + h),(255, 0, 0), 2)
    

cv2.imshow("Result", img)
cv2.waitKey(0)