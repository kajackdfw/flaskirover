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

        if 'camera_fpv_path' in start_settings:
            self.settings['camera_fpv_path'] = start_settings['camera_fpv_path']
        else:
            self.settings['camera_fpv_path'] = 'static/fpv'

        if 'camera_pictures_path' in start_settings:
            self.settings['camera_pictures_path'] = start_settings['camera_pictures_path']
        else:
            self.settings['camera_pictures_path'] = 'static/camera/pictures'

        if 'camera_thumbnail_path' in start_settings:
            self.settings['camera_thumbnail_path'] = start_settings['camera_thumbnail_path']
        else:
            self.settings['camera_thumbnail_path'] = 'static/camera/thumbnails'

        if 'camera_fpv_res_x' in start_settings:
            self.settings['camera_fpv_res_x'] = int(start_settings['camera_fpv_res_x'])
        else:
            self.settings['camera_fpv_res_x'] = 480

        if 'camera_fpv_res_y' in start_settings:
            self.settings['camera_fpv_res_y'] = int(start_settings['camera_fpv_res_y'])
        else:
            self.settings['camera_fpv_res_y'] = 320

        #  camera_photo_res_x
        if 'camera_photo_res_x' in start_settings:
            self.settings['camera_photo_res_x'] = int(start_settings['camera_photo_res_x'])
        else:
            self.settings['camera_photo_res_x'] = 800

        if 'camera_photo_res_y' in start_settings:
            self.settings['camera_photo_res_y'] = int(start_settings['camera_photo_res_y'])
        else:
            self.settings['camera_photo_res_y'] = 600

        self.settings['camera'] = 'active'


        try:
            self.camera = PiCamera()
            sleep(4)
            self.camera.resolution = (int(self.settings['camera_fpv_res_x']), int(self.settings['camera_fpv_res_y']))
            self.settings['camera_vflip'] = start_settings['camera_vflip']
            self.settings['camera_hflip'] = start_settings['camera_hflip']
            self.camera.vflip = self.settings['camera_vflip']
            self.camera.hflip = self.settings['camera_hflip']

        except NameError:
            print(" - No Picamera for Windows")
            self.settings['camera'] = 'disabled'
        except SystemError:
            print(" - Camera is probably not attached?")
            self.settings['camera'] = 'disabled'

    def take_fpv_image(self):
        if self.settings['camera'] == 'active':
            time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
            new_image_path_and_name = self.settings['camera_fpv_path'] + "/" + time_stamp + ".jpg"
            new_cam_image = open(new_image_path_and_name, 'wb')
            # camera.start_preview()
            try:
                #  self.camera.start_preview()
                self.camera.capture(new_cam_image)
                new_cam_image.close()
                return new_image_path_and_name
            except SystemError:
                new_cam_image.close()
                os.remove(new_image_path_and_name)
                return False

    def take_first_fpv_image(self):
        if self.settings['camera'] == 'active':
            time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
            self.camera.resolution = (self.settings['camera_fpv_res_x'] / 2, self.settings['camera_fpv_res_y'] / 2)
            new_image_path_and_name = self.settings['camera_fpv_path'] + "/" + time_stamp + ".jpg"
            new_cam_image = open(new_image_path_and_name, 'wb')
            # camera.start_preview()
            try:
                self.camera.start_preview()
                self.camera.capture(new_cam_image)
                new_cam_image.close()
                self.camera.resolution = (self.settings['camera_fpv_res_x'], self.settings['camera_fpv_res_y'])
                return new_image_path_and_name
            except SystemError:
                new_cam_image.close()
                os.remove(new_image_path_and_name)
                self.camera.resolution = (self.settings['camera_fpv_res_x'], self.settings['camera_fpv_res_y'])
                return False


    def take_picture(self):
        if self.settings['camera'] == 'active':
            time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
            new_image_path_and_name = self.settings['camera_pictures_path'] + "/" + time_stamp + ".jpg"
            # 2592x1944
            self.camera.resolution = (self.settings['camera_fpv_res_x'], self.settings['camera_fpv_res_y'])
            new_cam_image = open(new_image_path_and_name, 'wb')
            self.camera.start_preview()
            sleep(2)
            self.camera.capture(new_cam_image)
            new_cam_image.close()
            # restore web cam res
            self.camera.resolution = (int(self.settings['camera_fpv_res_x']), int(self.settings['camera_fpv_res_y']))
            return new_image_path_and_name

    def get_latest_web_cam_image(self):
        image_list = [f for f in listdir(self.settings['camera_fpv_path']) if isfile(join(self.settings['camera_fpv_path'], f))]
        last_timestamp = 0
        for image in image_list:
            filename_pieces = image.split('.')
            if int(filename_pieces[0]) > last_timestamp:
                last_timestamp = int(filename_pieces[0])
        last_filename = self.settings['camera_fpv_path'] + '/' + str(last_timestamp) + '.jpg'
        return last_filename

    def get_list_of_pictures(self):
        thumb_nail_list = [f for f in listdir(self.settings['camera_thumbnail_path']) if isfile(join(self.settings['camera_thumbnail_path'], f))]
        pictures = []
        picture_insert = 0
        for image in thumb_nail_list:
            filename_pieces = image.split('.')
            new_image = {
                'view_url': 'view/' + str(filename_pieces[0] + '.' + filename_pieces[1]),
                'thumbnail': self.settings['camera_thumbnail_path'] + '/' + filename_pieces[0] + '.' + filename_pieces[1]}
            pictures.insert(picture_insert, new_image)
        return pictures

    def set_awb(self, mode):
        if self.settings['camera'] == 'active':
            self.camera.awb_mode = mode
        return True

    def set_setting(self, setting_name, new_value, category, specs):
        print(str(specs))
        if not setting_name in specs:
            return 0
        else:
            old_value = self.settings[setting_name]
            print('  ? Old value = ' + old_value)
            if specs[setting_name]['type'] == 'int':
                self.settings[setting_name] = int(new_value)
            elif specs[setting_name]['type'] == 'float':
                self.settings[setting_name] = float(new_value)
            elif specs[setting_name]['type'] == 'bool' and new_value.uppercase() == 'TRUE':
                self.settings[setting_name] = True
            elif specs[setting_name]['type'] == 'bool' and new_value.uppercase() == 'FALSE':
                self.settings[setting_name] = False
            else:
                self.settings[setting_name] = new_value

            # Does this change need a page redraw
            if 'refresh' in specs[setting_name]:
                return 1
            else:
                return 0

    def get_settings(self):
        return self.settings
