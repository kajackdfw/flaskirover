from flask import Flask, render_template, url_for, request
import os
import sys
from subprocess import *
# from PIL import Image
import datetime
import time
import json
from picture_class import Picture
from configure import Configure

rover = Configure()

# FPV System
sys.path.append('hardware_drivers/vision')
if rover.config['camera'] == 'raspberry_pi_8mp' or rover.config['camera'] == 'raspberry_pi_5mp':
    from raspberry_pi_camera import Vision
else:
    print('Error : Rover requires some kind of vision!')
    exit()


# MOTOR System
sys.path.append('hardware_drivers/motor')
if rover.config['motor'] == 'adafruit_dc_and_stepper_motor_hat':
    from adafruit_dc_and_stepper_motor_hat import Motor
elif rover.config['motor'] == 'raspirobot_board_v3':
    from raspirobot_board_v3 import Motor
else:
    from immobile_wildlife_cam import Motor


# Gimbal for camera and fpv
if not rover.config['servo_camera_vert_number'] == -1 or not rover.config['servo_camera_horz_number'] == -1:
    sys.path.append('hardware_drivers/servo')
    if rover.config['servo'] == "adafruit_servo_hat":
        from adafruit_servo_hat import Servo
    elif rover.config['servo'] == "servos_using_wiringpi":
        from servos_using_wiringpi import Servo
    else:
        from no_servo import Servo
else:
    sys.path.append('hardware_drivers/servo')
    from no_servo import Servo

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
servo = Servo(rover.config)
for setting, val in servo.uis.items():
    uis[setting] = val
    print(' + ' + setting + ' = ' + str(val))

# http://flask.pocoo.org/snippets/67/

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
    path = picture.settings['camera_pictures_path']
    pic_info = picture.info(pic)
    uis['current'] = 'pictures'
    # print(str(pic_info))
    return render_template('picture.html', pic=pic, page_title='Picture : ' + pic, path=path, pic_info=pic_info, uis=uis)


@app.route('/settings')
def page_settings():
    uis['current'] = 'settings'

    # specs_fh = open("setting_specifications.json", "r")
    # specs = json.loads(str(specs_fh.read()))
    # specs_fh.close()

    specs = rover.get_setting_specifications()
    categories = rover.get_setting_categories()
    fields = rover.get_active_driver_settings()
    if not os.name == 'posix':
        # on Windows, refresh the CSS every minute of UI development, but hourly for Raspberry pi
        uis['time'] = '{:%Y%m%d%H%M}'.format(datetime.datetime.now())
    return render_template('settings.html', page_title='Settings', uis=uis, settings=rover.config, specs=specs, cats=categories, fields=fields)


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
    uis['servo_camera_vert_pos'] = servo.rotate_up(degrees)
    return str(uis['servo_camera_vert_pos'])


@app.route('/ajax/gimbal/center')
def gimbal_center():
    uis['servo_camera_vert_pos'] = servo.center()
    return str(uis['servo_camera_vert_pos'])


@app.route('/ajax/gimbal/rotate/down/<degrees>')
def gimbal_rotate_down(degrees):
    uis['servo_camera_vert_pos'] = servo.rotate_down(degrees)
    return str(uis['servo_camera_vert_pos'])


@app.route('/ajax/setting/set/<category>/<setting_name>/<new_value>')
def set_setting(category, setting_name, new_value):
    if category == setting_name:
        driver = new_value
        specs = rover.get_setting_specifications(category, driver)
        reset_required = motor.set_setting(setting_name, new_value, category, specs)
        setting_updates = motor.get_settings()
        rover.update_settings(setting_updates, category)
    return str(1)


@app.route('/stop')
def stop():
    motor.turn_off_motors()
    vision.take_fpv_image()
    latest_image = vision.get_latest_web_cam_image()
    uis['current'] = 'index'
    return render_template('drive.html', page_title='Home', image=latest_image, uis=uis)


@app.route('/quit')
def stop_server():
    servo.park()
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    time.sleep(5)
    # run_cmd('git pull')
    return "Quitting..."


@app.template_filter('uc_words')
def filter_uc_words(title):
    if len(title) == 0:
        return ' '
    else:
        title = title.replace('_', ' ')
        words = title.split(' ')
        new_string = ''
        for word in words:
            new_string += word.capitalize() + ' '
        return new_string.strip()


@app.template_filter('boolean')
def filter_boolean(some_value):
    if some_value == 1 or some_value is True or some_value.upper() == 'TRUE' or some_value.upper() == 'YES':
        return 'Yes'
    else:
        return 'No'


# cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    print(p.communicate()[0])
    return True


# use 8081 for server to avoid common Apache server at 8080 on dev env
if __name__ == '__main__' and os.name == 'posix':
    app.run(host='0.0.0.0', port=8080)
elif __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8082)

