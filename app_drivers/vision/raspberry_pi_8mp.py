import math
from os import listdir
from os.path import isfile, join
import os


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