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
  # Draw bounding boxes on the frame
  for detection in detections:
    box_points = detection['box_points']
    cv2.rectangle(frame, (box_points[0], box_points[1]), (box_points[2], box_points[3]), (0, 255, 0), 1)
    cv2.putText(
      frame,
      f"{detection['name']} {detection['percentage_probability']:.2f}%",
      (box_points[0], box_points[1] - 10),
      cv2.FONT_HERSHEY_SIMPLEX,
      0.4,
      (0, 255, 0),
      2
    )
  cv2.imshow('Video', frame)
  key = cv2.waitKey(1)
  if key == ord('q'):
    break

video.release()
cv2.destroyAllWindows()
