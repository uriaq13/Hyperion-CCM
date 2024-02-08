import cv2

##Open images
img = cv2.imread("path")

cv2.imshow("Output", img)
cv2.waitKey(0)

##Open video
# cap = cv2.VideoCapture("path")

# while True:
#     success, img = cap.read()
#     cv2.imshow("Video", img)
#     if cv2.waitKey(1) & 0XFF == ord('q'):
#         break
    
##Video capture
# cap = cv2.VideoCapture(0)
# #Resize image
# cap.set(3, 640)
# cap.set(4, 480)

# while True:
#     success, img = cap.read()
#     cv2.imshow("Video", img)
#     if cv2.waitKey(1) & 0XFF == ord('q'):
#         break
