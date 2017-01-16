import math
from os import listdir
from os.path import isfile, join
import os
from PIL import Image
import datetime


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

    def zoom_picture(self, pic_selected, zoom_factor, pan_x, pan_y):
        zoom_options = {}
        zoom_options['zoom'] = float(zoom_factor)

        path = self.settings['path_to_pictures']
        print('open ' + path + '/' + pic_selected)
        source_image = Image.open(path + '/' + pic_selected)
        print('format:' + str(source_image.format))
        print('size  : ' + str(source_image.size))
        print('mode  : ' + str(source_image.mode))

        width, height = source_image.size  # Get dimensions
        new_width = round(int(width) * zoom_options['zoom'], 0)
        new_height = round(int(height) * zoom_options['zoom'], 0)

        if new_width >= int(source_image.size[0]):
            new_width = int(source_image.size[0])
            new_height = round(new_width * 0.75, 0)
            zoom_options['zoom'] = 1.0
            zoom_options['zoom_out'] = 0
            zoom_options['zoom_in'] = 0.75
        elif new_width < int(self.settings['view_x']):
            new_width = int(self.settings['view_x'])
            new_height = int(self.settings['view_y'])
            zoom_options['zoom'] = new_width / int(source_image.size['x'])
            zoom_options['zoom_out'] = zoom_options['zoom'] + 0.25
            zoom_options['zoom_in'] = 0
        else:
            zoom_options['zoom_out'] = True
            zoom_options['zoom_in'] = True

        left = round((width - new_width) / 2, 0)
        top = round((height - new_height) / 2, 0)
        right = round((width + new_width) / 2, 0)
        bottom = round((height + new_height) / 2, 0)

        print(' new left = ' + str(left))
        print(' new top = ' + str(top))
        print(' new right = ' + str(right))
        print(' new bottom = ' + str(bottom))
        source_image = source_image.crop((left, top, right, bottom))

        # What will we call this new image
        time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
        file_name, extension = os.path.splitext(pic_selected)
        output_file = 'tmp/zoom_' + time_stamp + extension
        print('save to ' + output_file)
        source_image.save('static/' + output_file)
        zoom_options['file'] = output_file

        return zoom_options
