from flask import Flask, Response
import cv2

server_port = 5050
app = Flask(__name__)

# Camera resolution settings
resolutions = {
    'lo': (320, 240),
    'mid': (350, 530),
    'hi': (800, 600)
}

def generate_frames(resolution):
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/cam-lo.jpg')
def cam_lo():
    return Response(generate_frames(resolutions['lo']), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cam-mid.jpg')
def cam_mid():
    return Response(generate_frames(resolutions['mid']), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cam-hi.jpg')
def cam_hi():
    return Response(generate_frames(resolutions['hi']), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Starting web server...")
    print("Access the camera feed at:")
    print(f"  http://localhost:{server_port}/cam-lo.jpg")
    print(f"  http://localhost:{server_port}/cam-mid.jpg")
    print(f"  http://localhost:{server_port}/cam-hi.jpg")
    app.run(host='0.0.0.0', port=server_port)
