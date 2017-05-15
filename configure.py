import sys
import getopt
import json
import gc
import os


class Configure:

    def __init__(self):

        status = 'no_config'
        config = {}

        self.load()
        if self.status == 'invalid_config':
            print('Invalid configuration.json file, resetting to original test config.')
            self.reset()
            self.load()
            if self.status == 'invalid_config':
                print('Could not reset configuration.json file.')
                exit()

    def reset(self):
        self.config = {}
        self.config['config_name'] = 'default_afafruit_motor_hat_config'
        self.config['config_description'] = 'Default Afafruit Motor Hat Tank Config'
        self.config['drive_hat'] = 'adafruit_dc_and_stepper_motor_hat'
        self.config['drive_mode'] = 'tank'
        self.config['camera_res_x'] = 1056
        self.config['camera_res_y'] = 594
        self.config['camera_vflip'] = False
        self.config['camera_hflip'] = False
        self.config['ui_color'] = 'green'
        self.config['ui_size'] = 'lg4'
        self.config['fpv'] = 'raspberry_pi_8mp'
        self.config['camera'] = 'raspberry_pi_8mp'
        self.config['sensor_array'] = 'none'
        self.config['path_to_web_cam'] = 'static/fpv'
        self.config['sensor_array'] = 'none'

        # Adafruit_MotorHAT:
        #   FORWARD = 1
        #   BACKWARD = 2
        #   BRAKE = 3
        #   RELEASE = 4
        self.config['tank_left_forward'] = 1
        self.config['tank_right_forward'] = 1
        self.config['tank_left_reverse'] = 2
        self.config['tank_right_reverse'] = 2
        self.config['tank_left_motor'] = 1
        self.config['tank_right_motor'] = 2
        self.config['tank_speed_right'] = 155
        self.config['tank_speed_left'] = 145
        self.config['tank_turn_speed'] = 135

        # Camera Gimbal
        self.config['gimbal'] = "servos_using_wiringpi"
        self.config['gimbal_horz_servo_gpio'] = False

        # Available GPIO 4(p7), 17(p11) 27(p13) with AdaFruit Motor Hat
        self.config['gimbal_vert_servo_gpio'] = 17
        self.config['gimbal_vert_full_down'] = 50
        self.config['gimbal_vert_park'] = 125
        self.config['gimbal_vert_center'] = 125
        self.config['gimbal_vert_full_up'] = 250
        self.config['gimbal_vert_step'] = 10

        # This folder gets purged of old images often, only the last image is safe
        self.config['path_to_web_cam'] = 'static/fpv'

        # This can be redirected to ? a dropbox folder maybe?
        self.config['path_to_pictures'] = 'static/camera/photos'
        self.config['path_to_thumbnails'] = 'static/camera/thumbnails'

        config_fh = open('configuration.json', "w")
        config_fh.write(json.dumps(self.config, sort_keys=True, indent=4, separators=(',', ': ')))
        print('Config data saved in configuration.json \n')
        config_fh.close()

    def load(self):
        try:
            config_fh = open("configuration.json", "r")
            json_array_string = str(config_fh.read())
            self.config = json.loads(json_array_string)
            print(' + Config for ' + self.config['config_description'] + ' loaded')
            config_fh.close()
            # print(self.config)
            self.status = 'ready'
        except IOError:
            self.status = 'invalid_config'

    def setup(self):
        return True

    def get_uis_at_startup(self):
        uis = {}

        # Instrument Status
        uis['compass'] = 'disabled'
        uis['tilt'] = 'disabled'
        uis['battery'] = 'disabled'
        uis['thermometer'] = 'disabled'
        uis['sensors'] = 'disabled'
        uis['wifi'] = 'active'
        uis['drive'] = 'disabled'

        # Instrument Values
        uis['direction'] = 'fa-spin'
        uis['charge'] = '2'
        uis['temperature'] = '2'
        return uis
