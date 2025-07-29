from flask import Flask, render_template, Response
import cv2
import os

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

camera = cv2.VideoCapture(0)

# Treating the live video feed as a stream of images
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # ELECTRODE DETECTION LOGIC?

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Send stream of images/frames, stream of bytes (b)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5050)
    finally:
        camera.release()
        print('Camera released properly')
