import numpy as np
import cv2
import argparse
import imutils
from imutils.video import VideoStream
import time

# Parameter parsing
# python3 detect_faces_image.py --image assets/group.jpg --prototxt assets/deploy.prototxt --model assets/res10_300x300_ssd_iter_140000.caffemodel
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# Load the Caffe model
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# Load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Loop over the frames from the video stream
while True:
  # Grab the frame from the threaded video stream and resize it
  # to have a maximum width of 400 pixels
  frame = vs.read()
  frame = imutils.resize(frame, width=400)
  (h, w) = frame.shape[:2]
  blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300),
    (104.0, 177.0, 123.0))
  net.setInput(blob)
  detections = net.forward()

  # Loop over the detections
  for i in range(detections.shape[2]):
    # Extract the confidence (i.e., probability) associated with the prediction
    confidence = detections[0, 0, i, 2]
    # Filter out weak detections
    if confidence > args["confidence"]:
      # Compute the (x, y)-coordinates of the bounding box for the face
      box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
      (startX, startY, endX, endY) = box.astype("int")
      # Draw the bounding box and display the confidence
      text = "{:.2f}%".format(confidence * 100)
      y = startY - 15 if startY - 15 > 15 else startY + 15
      cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
      cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX,
        0.45, (255, 255, 255), 2)

  # Show the output frame
  cv2.imshow("Frame", frame)
  key = cv2.waitKey(1) & 0xFF
  # If the 'q' key was pressed, break from the loop
  if key == ord("q"):
    break

# Cleanup
vs.stop()
cv2.destroyAllWindows()
