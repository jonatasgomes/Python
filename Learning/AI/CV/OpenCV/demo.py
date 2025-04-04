import cv2
# import imutils

img = cv2.imread('assets/group.jpg', 0)
img = cv2.GaussianBlur(img, (1, 1), 0)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
