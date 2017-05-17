from flask import Flask, render_template, url_for, request
import os
import sys
from subprocess import *
# from PIL import Image
import datetime
import json
from picture_class import Picture
from configure import Configure

rover = Configure()

# FPV System
sys.path.append('hardware_drivers/vision')
if rover.config['fpv'] == 'raspberry_pi_8mp':
    from raspberry_pi_camera import Vision
else:
    print('Error : Rover requires some kind of vision!')
    exit()

# Gimbal for camera and fpv
if rover.config['gimbal_vert_servo_gpio'] is not False or rover.config['gimbal_horz_servo_gpio'] is not False:
    sys.path.append('hardware_drivers/gimbal')
    from servos_using_wiringpi import Gimbal


# MOTOR System
sys.path.append('hardware_drivers/motor')
if rover.config['drive_hat'] == 'adafruit_dc_and_stepper_motor_hat':
    from adafruit_dc_and_stepper_motor_hat import Motor
elif rover.config['drive_hat'] == 'raspirobot_board_v3':
    from raspirobot_board_v3 import Motor
else:
    from immobile_wildlife_cam import Motor


app = Flask(__name__, static_url_path='/static')
server_os = os.name

# User Interface Status
uis = rover.get_uis_at_startup()
uis['current'] = 'index'
uis['theme'] = "/static/css/theme-" + rover.config['ui_size'] + "-" + rover.config['ui_color'] + ".css"
uis['time'] = '{:%Y%m%d%H}'.format(datetime.datetime.now())

# CAMERA System
vision = Vision(rover.config)
uis['camera'] = vision.settings['camera']

# MOTOR SYSTEM
motor = Motor(rover.config)
uis['drive'] = motor.uis['drive']
uis['motor_speed'] = motor.uis['motor_speed']

# PICTURE GALLERY
picture = Picture(rover.config)

# Camera Gimbal
gimbal = Gimbal(rover.config)
for setting, val in gimbal.uis.items():
    uis[setting] = val


@app.route('/')
def page_index():
    vision.take_fpv_image()
    latest_image = vision.get_latest_web_cam_image()
    uis['current'] = 'index'
    uis['motor_speed'] = motor.uis['motor_speed']
    return render_template('drive.html', page_title='Home', image=latest_image, uis=uis)


@app.route('/new')
def page_new():
    vision.take_fpv_image()
    latest_image = vision.get_latest_web_cam_image()
    uis['current'] = 'new'
    return render_template('new.html', image=latest_image, uis=uis)


@app.route('/pictures')
def page_pictures():
    pictures = picture.get_list_of_pictures()
    uis['current'] = 'pictures'
    return render_template('pictures.html', page_title='Pictures', pictures=pictures, uis=uis)


@app.route('/picture/<pic>')
def page_picture(pic):
    # reset some picture class vars for a new image
    picture.settings['zoom'] = 1.0
    picture.settings['pan_x'] = 0
    picture.settings['pan_y'] = 0
    path = picture.settings['path_to_pictures']
    pic_info = picture.info(pic)
    uis['current'] = 'pictures'
    # print(str(pic_info))
    return render_template('picture.html', pic=pic, page_title='Picture : ' + pic, path=path, pic_info=pic_info, uis=uis)


@app.route('/settings')
def page_settings():
    uis['current'] = 'settings'
    # on Windows, refresh the CSS every time of UI development, but not for Rpi os
    # specs_fh = open("setting_specifications.json", "r")
    # specs = json.loads(str(specs_fh.read()))
    # specs_fh.close()
    specs = rover.get_setting_specifications()
    categories = rover.get_setting_categories()
    if not os.name == 'posix':
        uis['time'] = '{:%Y%m%d%H%M}'.format(datetime.datetime.now())
    return render_template('settings.html', page_title='Settings', uis=uis, settings=rover.config, specs=specs, cats=categories)


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
        vision.take_fpv_image()
        latest_image = vision.get_latest_web_cam_image()
        picture.clean_fpv_cache(latest_image)
    latest_image = vision.get_latest_web_cam_image()
    refresh_info = {}
    refresh_info['url'] = latest_image
    # print('latest = ' + latest_image)
    return json.dumps(refresh_info, separators=(',', ':'))


@app.route('/ajax/take_picture')
def take_picture():
    new_picture = vision.take_picture()
    picture.make_thumbnail(new_picture)
    return True


@app.route('/ajax/camera/color_mode/<mode>')
def set_white_balance(mode):
    return vision.set_awb(mode)


@app.route('/ajax/motor/forward/crawl/<seconds>')
def motor_crawl(seconds):
    motor.forward_crawl(seconds)
    vision.take_first_fpv_image()
    return True


@app.route('/ajax/motor/backward/crawl/<seconds>')
def motor_crawl_back(seconds):
    motor.backward_crawl(seconds)
    vision.take_first_fpv_image()
    return True


@app.route('/ajax/motor/rotate/ccw/<second_hundredths>')
def motor_rotate_ccw(second_hundredths):
    motor.rotate_ccw(second_hundredths)
    vision.take_first_fpv_image()
    return True


@app.route('/ajax/motor/rotate/cw/<second_hundredths>')
def motor_rotate_cw(second_hundredths):
    motor.rotate_cw(second_hundredths)
    vision.take_first_fpv_image()
    return True


@app.route('/ajax/motor/speed/<multiplier>')
def motor_speed(multiplier):
    motor.speed_adjust(multiplier)
    return True


@app.route('/ajax/gimbal/rotate/up/<degrees>')
def gimbal_rotate_up(degrees):
    gimbal.rotate_up(degrees)
    return True


# 192.168.1.12 - - [14/May/2017 20:52:36] "GET /ajax/gimbal/rotate/up/10 HTTP/1.1" 500 -
@app.route('/ajax/gimbal/rotate/down/<degrees>')
def gimbal_rotate_down(degrees):
    gimbal.rotate_down(degrees)
    return True


@app.route('/ajax/gimbal/center')
def gimbal_center():
    gimbal.center()
    return True


@app.route('/stop')
def stop():
    motor.turn_off_motors()
    vision.take_fpv_image()
    latest_image = vision.get_latest_web_cam_image()
    uis['current'] = 'index'
    return render_template('drive.html', page_title='Home', image=latest_image, uis=uis)


@app.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    run_cmd('git pull')
    return "Quitting..."


# cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    print(p.communicate()[0])
    return True


if __name__ == '__main__' and os.name == 'posix':
    app.run(host='0.0.0.0', port=8080)
elif __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8080)

