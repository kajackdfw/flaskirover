from flask import Flask, render_template, url_for
import os
import sys
from PIL import Image
import datetime
import json
from picture_class import Picture

sys.path.append('hardware_drivers/vision')
from raspberry_pi_8mp import Vision  # change raspberry_pi_8mp to match your hardware

sys.path.append('hardware_drivers/motor')
from adafruit_dc_and_stepper_motor_hat import Motor  # change to match your motor hat

app = Flask(__name__, static_url_path='/static')
server_os = os.name
startup_settings = {}

startup_settings['view_x'] = 920
startup_settings['view_y'] = round(startup_settings['view_x'] * 0.75, 0)

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
picture = Picture(startup_settings)


@app.route('/')
def page_index():
    return render_template('index.html', page_title='Home')


@app.route('/drive')
def page_drive():
    latest_image = vision.get_latest_web_cam_image()
    return render_template('drive.html', image=latest_image)


@app.route('/pictures')
def page_pictures():
    pictures = picture.get_list_of_pictures()
    return render_template('pictures.html', page_title='Pictures', pictures=pictures)


@app.route('/status')
def page_status():
    about_info = {'status': 'incomplete', 'access': 'private wifi'}
    latest_image = vision.get_latest_web_cam_image()
    return render_template('status.html', page_title='Status', image=latest_image, about_info=about_info)


@app.route('/view/<image>')
def page_view(image):
    picture.settings['zoom'] = 1.0
    picture.settings['pan_x'] = 0
    picture.settings['pan_y'] = 0
    path = picture.settings['path_to_pictures']
    pic_info = picture.info(image)
    return render_template('picture.html', page_title='Picture : ' + image, image=image, path=path, pic_info=pic_info)


@app.route('/about')
def page_about():
    return render_template('about.html', page_title=' / About RaspRover')


@app.route('/ajax/zoom/<image_file>/<zoom_factor>')
def zoom_image(image_file, zoom_factor):
    zoom_info = picture.zoom(image_file, zoom_factor)
    zoom_info['url'] = url_for('static', filename=zoom_info['file'])
    return json.dumps(zoom_info, separators=(',', ':'))


@app.route('/ajax/pan/<image_file>/<pan_direction>')
def pan_image(image_file, pan_direction):
    pan_info = picture.pan(image_file, pan_direction)
    pan_info['url'] = url_for('static', filename=pan_info['file'])
    return json.dumps(pan_info, separators=(',', ':'))


if __name__ == '__main__' and os.name == 'posix':
    app.run(debug=True, host='0.0.0.0')
elif __name__ == '__main__':
    app.run(debug=True, host='localhost')

