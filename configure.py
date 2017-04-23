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
        self.config['description'] = 'Afafruit Motor Hat Tank Config'
        self.config['motor_hat'] = 'adafruit_dc_and_stepper_motor_hat'
        self.config['drive_mode'] = 'tank'
        self.config['view_x'] = 1056
        self.config['view_y'] = 594
        self.config['view_optimize'] = 'LG G4'
        self.config['theme'] = 'green'
        self.config['fpv'] = 'raspberry_pi_8mp'
        self.config['camera'] = 'raspberry_pi_8mp'
        self.config['sensor_array'] = 'none'
        self.config['path_to_web_cam'] = 'static/fpv'
        self.config['sensor_array'] = 'none'
        self.config['tank_left_motor'] = 3
        self.config['tank_right_motor'] = 4
        self.config['tank_speed_right'] = 125
        self.config['tank_speed_left'] = 135
        self.config['tank_turn_speed'] = 110
        # Adafruit_MotorHAT:
        #   FORWARD = 1
        #   BACKWARD = 2
        #   BRAKE = 3
        #   RELEASE = 4
        self.config['tank_left_forward'] = 1
        self.config['tank_right_forward'] = 2
        self.config['tank_left_reverse'] = 2
        self.config['tank_right_reverse'] = 1

        # Camera Gimbal
        # Available GPIOs ( 4, 17, 18, 22-25, 27 ) with AdaFruit Motor Hat
        self.config['gimbal_horz_servo_gpio'] = False

        self.config['gimbal_vert_servo_gpio'] = 23
        self.config['gimbal_vert_full_down'] = -15
        self.config['gimbal_vert_center'] = 0
        self.config['gimbal_vert_full_up'] = 15
        self.config['gimbal_vert_up'] = 1
        self.config['gimbal_vert_down'] = -1

        if os.path.isdir('static/fpv'):
            self.config['path_to_web_cam'] = 'static/fpv'
            self.config['path_to_pictures'] = 'static/camera/photos'
            self.config['path_to_thumbnails'] = 'static/camera/thumbnails'
        else:
            # We can function without the std directories, but all photos will be lost in tmp
            self.config['path_to_web_cam'] = '/tmp/static/fpv'
            self.config['path_to_pictures'] = '/tmp/static/camera/photos'
            self.config['path_to_thumbnails'] = '/tmp/static/camera/thumbnails'

        config_fh = open('configuration.json', "w")
        config_fh.write(json.dumps(self.config, sort_keys=True, indent=4, separators=(',', ': ')))
        print('Config data saved in configuration.json \n')
        config_fh.close()

    def load(self):
        try:
            config_fh = open("configuration.json", "r")
            json_array_string = str(config_fh.read())
            self.config = json.loads(json_array_string)
            print('  + Config for ' + self.config['description'] + ' loaded')
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
