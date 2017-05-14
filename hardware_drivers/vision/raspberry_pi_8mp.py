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
    print(" - No Picamera Library installed.")


class Vision:

    settings = {}

    def __init__(self, start_settings):

        if 'path_to_web_cam' in start_settings:
            self.settings['path_to_web_cam'] = start_settings['path_to_web_cam']
        else:
            self.settings['path_to_web_cam'] = 'static/fpv'

        if 'path_to_pictures' in start_settings:
            self.settings['path_to_pictures'] = start_settings['path_to_pictures']
        else:
            self.settings['path_to_pictures'] = 'static/camera/pictures'

        if 'path_to_thumbnails' in start_settings:
            self.settings['path_to_thumbnails'] = start_settings['path_to_thumbnails']
        else:
            self.settings['path_to_thumbnails'] = 'static/camera/thumbnails'

        if 'camera_res_x' in start_settings:
            self.settings['camera_res_x'] = int(start_settings['camera_res_x'])
        else:
            self.settings['camera_res_x'] = 800

        if 'camera_res_y' in start_settings:
            self.settings['camera_res_y'] = int(start_settings['camera_res_y'])
        else:
            self.settings['camera_res_y'] = 600

        self.settings['camera'] = 'active'


        try:
            self.camera = PiCamera()
            sleep(4)
            self.camera.resolution = (int(self.settings['camera_res_x']), int(self.settings['camera_res_y']))
            self.settings['camera_vflip'] = self.settings['camera_vflip']
            self.settings['camera_hflip'] = self.settings['camera_hflip']

        except NameError:
            print(" - No Picamera for Windows")
            self.settings['camera'] = 'disabled'
        except SystemError:
            print(" - Camera is probably not attached?")
            self.settings['camera'] = 'disabled'

    def take_web_cam_image(self):
        if self.settings['camera'] == 'active':
            time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
            new_image_path_and_name = self.settings['path_to_web_cam'] + "/" + time_stamp + ".jpg"
            new_cam_image = open(new_image_path_and_name, 'wb')
            # camera.start_preview()
            try:
                self.camera.start_preview()
                self.camera.vflip = True
                self.camera.hflip = True
                self.camera.capture(new_cam_image)
            except SystemError:
                new_cam_image.close()
                os.remove(new_image_path_and_name)

            new_cam_image.close()

    def take_picture(self):
        if self.settings['camera'] == 'active':
            time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
            new_image_path_and_name = self.settings['path_to_pictures'] + "/" + time_stamp + ".jpg"
            # 2592x1944
            self.camera.resolution = (2592, 1944)
            new_cam_image = open(new_image_path_and_name, 'wb')
            self.camera.start_preview()
            self.camera.vflip = True
            self.camera.hflip = True
            sleep(1)
            self.camera.capture(new_cam_image)
            new_cam_image.close()
            # restore web cam res
            self.camera.resolution = (int(self.settings['camera_res_x']), int(self.settings['camera_res_y']))
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

    def set_awb(self, mode):
        if self.settings['camera'] == 'active':
            self.camera.awb_mode = mode
        return True
