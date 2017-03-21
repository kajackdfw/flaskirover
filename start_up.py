import sys
import getopt
import json
import gc
import os


class Startup:

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
        self.config['view_x'] = 1056
        self.config['view_y'] = 594
        self.config['view_optimize'] = 'LG G4'
        self.config['theme'] = 'green'
        self.config['motor_hat'] = 'adafruit_dc_and_stepper_motor_hat'
        self.config['motor_hat_mode'] = 'tank'
        self.config['fpv'] = 'raspberry_pi_8mp'
        self.config['camera'] = 'raspberry_pi_8mp'
        self.config['sensor_array'] = 'none'
        self.config['path_to_web_cam'] = 'static/webcam'

        if os.path.isdir('static/webcam'):
            self.config['path_to_web_cam'] = 'static/webcam'
            self.config['path_to_pictures'] = 'static/camera/photos'
            self.config['path_to_thumbnails'] = 'static/camera/thumbnails'
        else:
            # We can function without the std directories, but all photos will be lost in tmp
            self.config['path_to_web_cam'] = '/tmp/static/webcam'
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
            print('Config for ' + self.config['description'] + ' loaded')
            config_fh.close()
            print(self.config)
            self.status = 'ready'
        except IOError:
            self.status = 'invalid_config'

    def setup(self):
        return True
