import cv2
from imageai.Detection import ObjectDetection
import os

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(os.path.join(os.path.dirname(__name__), 'assets/tiny-yolo-v3.pt'))
detector.loadModel()

video = cv2.VideoCapture('assets/road_traffic_01.mp4')
while True:
  ret, frame = video.read()
  if not ret:
    break
  custom_objs = detector.CustomObjects(car=True)
  detected_img, detections, extra_obj = detector.detectObjectsFromImage(
    input_image=frame, output_type="array",
    custom_objects=custom_objs,
    display_percentage_probability=False,
    extract_detected_objects=True,
    minimum_percentage_probability=30
  )
  cv2.imshow('Video', detected_img)
  key = cv2.waitKey(1)
  if key == ord('q'):
    break

video.release()
cv2.destroyAllWindows()
