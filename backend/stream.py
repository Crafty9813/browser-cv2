from flask import Flask, render_template, Response
import cv2

app = Flask(__name__, template_folder='../frontend/templates')

camera = cv2.VideoCapture(0)

def generate_frames():
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                # ELECTRODE DETECTION LOGIC
                # frame = detect_electrodes(frame)

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                # Send stream of images/frames, stream of bytes (b)
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                
    except GeneratorExit:
        print("Client left")
    finally:
        camera.release()

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
