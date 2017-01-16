from flask import Flask, render_template, url_for
import os
import sys
from PIL import Image
import datetime
import json


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


@app.route('/')
def index():
    pictures = vision.get_list_of_pictures()
    return render_template('index.html', pictures=pictures)


@app.route('/view/<image>')
def view(image):
    path = vision.settings['path_to_pictures']
    return render_template('view.html', image=image, path=path)


@app.route('/get/<image_file>/<zoom_in>/<x>/<y>')
def get_image(image_file,zoom_in,x,y):
    # path = vision.settings['path_to_pictures']
    # print('open ' + path + '/' + image_file)
    # source_image = Image.open(path + '/' + image_file)
    # print('format:' + str(source_image.format))
    # print('size  : ' + str(source_image.size))
    # print('mode  : ' + str(source_image.mode))
    #
    # width, height = source_image.size  # Get dimensions
    # new_width = width * 0.75
    # new_height = height * 0.75
    # left = round((width - new_width) / 2 , 0)
    # top = round((height - new_height) / 2, 0)
    # right = round((width + new_width) / 2, 0)
    # bottom = round((height + new_height) / 2, 0)
    # print(' new left = ' + str(left))
    # print(' new top = ' + str(top))
    # print(' new right = ' + str(right))
    # print(' new bottom = ' + str(bottom))
    # source_image = source_image.crop((left, top, right, bottom))
    #
    # # What will we call this new image
    # time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    # file_name, extension = os.path.splitext(image_file)
    # output_file = 'tmp/zoom_' + time_stamp + extension
    # print('save to ' + output_file)
    # source_image.save('static/' + output_file)
    zoom_info = vision.zoom_picture(image_file, zoom_in, x, y)
    zoom_info['url'] = url_for('static', filename=zoom_info['file'])
    return json.dumps(zoom_info, separators=(',',':'))


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

