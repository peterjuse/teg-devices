from flask import Flask, render_template, Response
from time import sleep

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        # frame = camara.get_frame()
        # cv2.imwrite('pic.jpg', frame) 
        sleep(0.3)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + \
                open('pic.jpg', 'rb').read() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True)
