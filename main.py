from flask import Flask, render_template, Response
import cv2
import socket

app = Flask(__name__)
camera = cv2.VideoCapture(0) # Camera Selected

def gen_frames():  # Frame Recording
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
            # ¯\_(ツ)_/¯

@app.route('/') # Main Page
def index():
    return render_template('index.html')

@app.route('/video_feed') # Camera Page
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    app.run(debug=True, host= local_ip) # Flask Server