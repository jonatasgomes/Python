import cv2
import torch
import numpy as np
import urllib
import pathlib
from pathlib import Path
import certifi
import os

# Set SSL certificate file
os.environ['SSL_CERT_FILE'] = certifi.where()

# pathlib.PosixPath = pathlib.WindowsPath

path = '/Users/jonatas/Apps/Python/Learning/AI/Yolo/image-detection/pigs/run_1/weights/best.pt'
image_url = 'http://127.0.0.1:5000/image'

model = torch.hub.load('ultralytics/yolov5', 'custom', path, force_reload=True)
model.conf = 0.6 #essa variável determina a acurácia do seu modelo. Faça testes para encontrar o melhor resultado.

print(path)

while True:
    img_resp=urllib.request.urlopen(url=image_url)
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    im = cv2.imdecode(imgnp,-1)
    results = model(im)
    print(results)
    frame = np.squeeze(results.render())
    cv2.imshow('Deteccao', frame)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break

cv2.destroyAllWindows()
