from flask import Flask, render_template, url_for, request
import os
import sys
from subprocess import *
from PIL import Image
import datetime
import json
from picture_class import Picture
from start_up import Startup

startup = Startup()

# FPV System
sys.path.append('hardware_drivers/vision')
if startup.config['fpv'] == 'raspberry_pi_8mp':
    from raspberry_pi_8mp import Vision  # change raspberry_pi_8mp to match your hardware
else:
    print('Error : Rover requires some kind of vision!')
    exit()

# MOTOR System
sys.path.append('hardware_drivers/motor')
if startup.config['motor_hat'] == 'adafruit_dc_and_stepper_motor_hat':
    from adafruit_dc_and_stepper_motor_hat import Motor
elif startup.config['motor_hat'] == 'raspirobot_board_v3':
    from raspirobot_board_v3 import Motor
elif startup.config['motor_hat'] == 'immobile_wildlife_cam':
    from immobile_wildlife_cam import Motor


app = Flask(__name__, static_url_path='/static')
server_os = os.name

uis = {}
# Instrument Status
uis['compass'] = 'disabled'
uis['tilt'] = 'disabled'
uis['battery'] = 'disabled'
uis['thermometer'] = 'disabled'
uis['sensors'] = 'disabled'
uis['wifi'] = 'active'
uis['drive'] = 'active'

# Instrument Values
uis['direction'] = 'fa-spin'
uis['charge'] = '2'
uis['temperature'] = '2'
uis['current'] = 'index'

status_dic = {
    'code': 'incomplete',
    'access': 'private wifi'
    # 'os': str(os.environ['OS'])
}


# CAMERA System
vision = Vision(startup.config)
uis['camera'] = vision.settings['camera']

motor = Motor(startup.config)
# uis['drive'] = motor.settings['drive']

picture = Picture(startup.config)


@app.route('/')
def page_index():
    vision.take_web_cam_image()
    latest_image = vision.get_latest_web_cam_image()
    uis['current'] = 'index'
    return render_template('drive.html', page_title='Home', image=latest_image, uis=uis)


@app.route('/new')
def page_new():
    vision.take_web_cam_image()
    latest_image = vision.get_latest_web_cam_image()
    uis['current'] = 'new'
    return render_template('new.html', image=latest_image, uis=uis)


@app.route('/pictures')
def page_pictures():
    pictures = picture.get_list_of_pictures()
    uis['current'] = 'pictures'
    return render_template('pictures.html', page_title='Pictures', pictures=pictures, uis=uis)


@app.route('/view/<pic>')
def page_picture(pic):
    # reset some picture class vars for a new image
    picture.settings['zoom'] = 1.0
    picture.settings['pan_x'] = 0
    picture.settings['pan_y'] = 0

    path = picture.settings['path_to_pictures']
    pic_info = picture.info(pic)
    uis['current'] = 'pictures'
    print(str(pic_info))
    return render_template('picture.html', pic=pic, page_title='Picture : ' + pic, path=path, pic_info=pic_info, uis=uis)


@app.route('/about')
def page_about():
    uis['current'] = 'about'
    return render_template('about.html', page_title=' / About RaspRover', uis=uis)


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


@app.route('/ajax/view_refresh')
def view_refresh():
    if vision.settings['camera'] == 'active':
        vision.take_web_cam_image()
        latest_image = vision.get_latest_web_cam_image()
        picture.clean_webcam_cache(latest_image)
    latest_image = vision.get_latest_web_cam_image()
    refresh_info = {}
    refresh_info['url'] = latest_image
    print('latest = ' + latest_image)
    return json.dumps(refresh_info, separators=(',', ':'))


@app.route('/ajax/take_picture')
def take_picture():
    new_picture = vision.take_picture()
    picture.make_thumbnail(new_picture)
    return True


@app.route('/ajax/camera/awb_mode/<mode>')
def set_white_balance(mode):
    return vision.set_awb(mode)


@app.route('/ajax/motor/forward/crawl/<seconds>')
def motor_crawl(seconds):
    motor.forward_crawl(seconds)
    vision.take_web_cam_image()
    return True


@app.route('/ajax/motor/backward/crawl/<seconds>')
def motor_crawl_back(seconds):
    motor.backward_crawl(seconds)
    vision.take_web_cam_image()
    return True


@app.route('/ajax/motor/rotate/ccw/<second_hundredths>')
def motor_rotate_ccw(second_hundredths):
    motor.rotate_ccw(second_hundredths)
    vision.take_web_cam_image()
    return True


@app.route('/ajax/motor/rotate/cw/<second_hundredths>')
def motor_rotate_cw(second_hundredths):
    motor.rotate_cw(second_hundredths)
    vision.take_web_cam_image()
    return True


# cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    print(p.communicate()[0])
    return True


@app.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    run_cmd('git pull')
    return "Quitting..."


if __name__ == '__main__' and os.name == 'posix':
    app.run(host='0.0.0.0', port=8080)
elif __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8080)

