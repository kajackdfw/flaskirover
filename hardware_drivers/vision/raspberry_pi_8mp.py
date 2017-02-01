import math
from os import listdir
from os.path import isfile, join
import os
from PIL import Image
import datetime
from time import sleep

try:
    from picamera import PiCamera
except ImportError:
    print("  No Picamera Import for Windows")


class Vision:

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

        if 'view_x' in start_settings:
            self.settings['view_x'] = int(start_settings['view_x'])
        else:
            self.settings['view_x'] = 800

        if 'view_y' in start_settings:
            self.settings['view_y'] = int(start_settings['view_y'])
        else:
            self.settings['view_x'] = 600

        try:
            self.camera = PiCamera()
            self.camera.resolution = (int(self.settings['view_x']), int(self.settings['view_y']))
            sleep(2)
        except NameError:
            print("  No Picamera for Windows")
            self.settings['no_camera'] = True
        except SystemError:
            print("  Camera is probably not attached?")
            self.settings['no_camera'] = True

    def take_web_cam_image(self):
        if 'no_camera' not in self.settings:
            time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
            new_image_path_and_name = self.settings['path_to_web_cam'] + "/" + time_stamp + ".jpg"
            new_cam_image = open(new_image_path_and_name, 'wb')
            # camera.start_preview()
            self.camera.capture(new_cam_image)
            new_cam_image.close()

    def take_picture(self):
        if 'no_camera' not in self.settings:
            time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
            new_image_path_and_name = self.settings['path_to_pictures'] + "/" + time_stamp + ".jpg"
            # 2592x1944
            self.camera.resolution = (2592, 1944)
            new_cam_image = open(new_image_path_and_name, 'wb')
            self.camera.capture(new_cam_image)
            new_cam_image.close()
            # restore web cam res
            self.camera.resolution = (int(self.settings['view_x']), int(self.settings['view_y']))
            return new_image_path_and_name

    def get_latest_web_cam_image(self):
        image_list = [f for f in listdir(self.settings['path_to_web_cam']) if isfile(join(self.settings['path_to_web_cam'], f))]
        last_timestamp = 0
        for image in image_list:
            filename_pieces = image.split('.')
            if int(filename_pieces[0]) > last_timestamp:
                last_timestamp = int(filename_pieces[0])
        last_filename = self.settings['path_to_web_cam'] + '/' + str(last_timestamp) + '.jpg'
        return last_filename

    def get_list_of_pictures(self):
        thumb_nail_list = [f for f in listdir(self.settings['path_to_thumbnails']) if isfile(join(self.settings['path_to_thumbnails'], f))]
        pictures = []
        picture_insert = 0
        for image in thumb_nail_list:
            filename_pieces = image.split('.')
            new_image = {
                'view_url': 'view/' + str(filename_pieces[0] + '.' + filename_pieces[1]),
                'thumbnail': self.settings['path_to_thumbnails'] + '/' + filename_pieces[0] + '.' + filename_pieces[1]}
            pictures.insert(picture_insert, new_image)
        return pictures


