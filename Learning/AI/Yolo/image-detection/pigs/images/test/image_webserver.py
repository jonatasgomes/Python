from flask import Flask, send_file
import os
import time
import threading

directory = "./"  # Change this to your target folder
app = Flask(__name__)
images = []
current_index = 0

def update_image_list():
    global images
    while True:
        images = [f for f in os.listdir(directory) if f.lower().endswith(".jpg")]
        time.sleep(2)  # Update the list every 2 seconds

def image_rotation():
    global current_index
    while True:
        if images:
            current_index = (current_index + 1) % len(images)
        time.sleep(5)  # Rotate every 5 seconds

@app.route('/image')
def serve_image():
    if not images:
        return "No images found", 404
    image_path = os.path.join(directory, images[current_index])
    return send_file(image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    if not os.path.exists(directory):
        os.makedirs(directory)
    threading.Thread(target=update_image_list, daemon=True).start()
    threading.Thread(target=image_rotation, daemon=True).start()
    app.run(host='127.0.0.1', port=5000, debug=False)
