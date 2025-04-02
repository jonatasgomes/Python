import cv2
from matplotlib import pyplot as plt

img = cv2.imread('assets/stop_sign.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

stop_data = cv2.CascadeClassifier('assets/stop_sign_cascade.xml')
found = stop_data.detectMultiScale(img_gray, minSize=(20, 20))
amount_found = len(found)
print("Found: ", amount_found)

if amount_found > 0:
  for x, y, w, h in found:
    cv2.rectangle(img_rgb, (x, y), (x + h, y + w), (0, 255, 0), 5)

plt.subplot(1, 1, 1)
plt.imshow(img_rgb)
plt.show()
