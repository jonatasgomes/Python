import cv2
import random

cap = cv2.VideoCapture(0)
point = (100, 100)
color = (0, 255, 0)
count = 0

while True:
  ret, frame = cap.read()
  if not ret:
    break
  cv2.flip(frame, 1, frame)
  cv2.rectangle(frame, (100, 100), (200, 200), (0, 255, 0), 3)
  count += 1
  if count % 20 == 0:
    point = (random.randint(0, frame.shape[1]), random.randint(0, frame.shape[0]))
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
  cv2.circle(frame, point, 50, color, -1)
  cv2.putText(frame, 'Hello, OpenCV!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
  cv2.imshow('frame', frame)
  if cv2.waitKey(1) == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
