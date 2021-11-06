from productivity import app
from flask import render_template, Response
from productivity.cam import camera, gen_frames

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')