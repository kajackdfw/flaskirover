# flaskenrover is for a Raspberry Pi camera and a AdaFruit Motor Hat combination.
# If you have a different camera, fork this page to whatever_camera.py and add your own camera code.
# If you have a different motor system, fork this page to whatever_motor.py and add your own motor code.
# app.py has separate objects for motor and camera classes if needed. Look for > Plugin the hardware driver classes here

import math
from os import listdir
from os.path import isfile, join
import os

class Rover:

    settings = {}

    # startup_settings['path_to_webcam'] = '/tmp/static/webcam'
    # startup_settings['path_to_pictures'] = '/tmp/static/camera/photos'
    # startup_settings['path_to_thunbnails'] = '/tmp/static/camera/thumbnails'

    def __init__(self, start_settings):

        if 'path_to_web_cam' in start_settings:
            self.settings['path_to_web_cam'] = start_settings['path_to_web_cam']
        else:
            self.settings['path_to_web_cam'] = 'static/webcam'

        if 'path_to_pictures' in start_settings:
            self.settings['path_to_pictures'] = start_settings['path_to_pictures']
        else:
            self.settings['path_to_pictures'] = 'static/camera/pictures'

        if 'path_to_thumbnails' in start_settings:
            self.settings['path_to_thumbnails'] = start_settings['path_to_thumbnails']
        else:
            self.settings['path_to_thumbnails'] = 'static/camera/thumbnails'

    def get_latest_web_cam_image(self):
        image_list = [f for f in listdir(self.settings['path_to_web_cam']) if isfile(join(self.settings['path_to_web_cam'], f))]
        last_timestamp = 0
        for image in image_list:
            filename_pieces = image.split('.')
            if int(filename_pieces[0]) > last_timestamp:
                last_timestamp = int(filename_pieces[0])
        last_filename = self.settings['path_to_web_cam'] + '/' + str(last_timestamp) + '.jpg'
        return last_filename
