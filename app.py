from flask import Flask, render_template
import os
import sys

sys.path.append('hardware_drivers/vision')
from raspberry_pi_8mp import Vision  # change raspberry_pi_8mp to match your hardware

sys.path.append('hardware_drivers/motor')
from adafruit_dc_and_stepper_motor_hat import Motor  # change to match your motor hat

app = Flask(__name__)
server_os = os.name
startup_settings = {}

if os.path.isdir('static/webcam'):
    startup_settings['path_to_web_cam'] = 'static/webcam'
    startup_settings['path_to_pictures'] = 'static/camera/photos'
    startup_settings['path_to_thumbnails'] = 'static/camera/thumbnails'
else:
    # We can function without the std directories, but all photos will be lost in tmp
    startup_settings['path_to_web_cam'] = '/tmp/static/webcam'
    startup_settings['path_to_pictures'] = '/tmp/static/camera/photos'
    startup_settings['path_to_thumbnails'] = '/tmp/static/camera/thumbnails'

# Plugin the hardware drivers here
vision = Vision(startup_settings)
motor = Motor(startup_settings)


@app.route('/')
def index():
    pictures = vision.get_list_of_pictures()
    return render_template('index.html', pictures=pictures)


@app.route('/view/<image>')
def view(image):
    path = vision.settings['path_to_pictures']
    return render_template('view.html', image=image, path=path)


@app.route('/drive')
def drive():
    latest_image = vision.get_latest_web_cam_image()
    return render_template('drive.html', image=latest_image)


@app.route('/test/<image>')
def test(image):
    path = vision.settings['path_to_pictures']
    return render_template('view_with_canvas_and_mouse.html', image=image, path=path)


if __name__ == '__main__' and os.name == 'posix':
    app.run(debug=True, host='0.0.0.0')
elif __name__ == '__main__':
    app.run(debug=True, host='localhost')

