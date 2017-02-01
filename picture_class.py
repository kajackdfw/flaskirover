import math
from os import listdir
from os.path import isfile, join
import os
from PIL import Image
import datetime


class Picture:

    settings = {}

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

        self.settings['zoom'] = 1.0
        self.clean_tmp()

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

    def zoom(self, pic_selected, zoom_factor):
        zoom_options = {}
        if float(zoom_factor) >= 1:
            zoom_options['zoom'] = 1.0
            self.settings['zoom'] = zoom_options['zoom']
            self.settings['pan_x'] = 0
            self.settings['pan_y'] = 0
        else:
            zoom_options['zoom'] = float(zoom_factor)
            self.settings['zoom'] = zoom_options['zoom']

        path = self.settings['path_to_pictures']
        source_image = Image.open(path + '/' + pic_selected)
        print('image size  : ' + str(source_image.size))

        width, height = source_image.size  # Get dimensions
        new_width = round(int(width) * zoom_options['zoom'], 0)
        new_height = round(int(height) * zoom_options['zoom'], 0)
        zoom_options['y_aspect'] = float(int(source_image.size[1]) / int(source_image.size[0]))

        if new_width >= int(source_image.size[0]):
            new_width = int(source_image.size[0])
            new_height = round(new_width * zoom_options['y_aspect'], 0)
            zoom_options['zoom'] = 1.0
            zoom_options['zoom_out'] = 0
            zoom_options['zoom_in'] = 0.75
        elif new_width < int(self.settings['view_x']):
            new_width = int(self.settings['view_x'])
            new_height = int(self.settings['view_x'] * zoom_options['y_aspect'])
            zoom_options['zoom'] = new_width / int(source_image.size[0])
            zoom_options['zoom_out'] = zoom_options['zoom'] + 0.25
            zoom_options['zoom_in'] = 0
        else:
            zoom_options['zoom_out'] = True
            zoom_options['zoom_in'] = True

        self.settings['zoom'] = zoom_options['zoom']

        # select view region
        left = int(round((width - new_width) / 2, 0) + self.settings['pan_x'])
        top = int(round((height - new_height) / 2, 0) + self.settings['pan_y'])
        right = int(round((width + new_width) / 2, 0) + self.settings['pan_x'])
        bottom = int(round((height + new_height) / 2, 0) + self.settings['pan_y'])
        source_image = source_image.crop((left, top, right, bottom))

        # What will we call this new image
        time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
        file_name, extension = os.path.splitext(pic_selected)
        output_file = 'tmp/zoom_' + time_stamp + extension
        source_image.save('static/' + output_file)
        zoom_options['file'] = output_file
        return zoom_options

    def pan(self, current_image, pan_direction):
        pan_results = {}

        if self.settings['zoom'] >= 1.0:

            # reset the pan settings
            self.settings['zoom'] = 1.0
            self.settings['pan_x'] = 0
            self.settings['pan_y'] = 0

            pan_results['zoom'] = 1.0
            pan_results['file'] = self.settings['path_to_pictures'] + current_image
            pan_results['zoom_out'] = False
            pan_results['zoom_in'] = True
            return pan_results
        else:
            pan_results['zoom'] = self.settings['zoom']

        # ok to pan
        path = self.settings['path_to_pictures']
        source_image = Image.open(path + '/' + current_image)
        width, height = source_image.size  # Get dimensions
        pan_results['y_aspect'] = float(int(source_image.size[1]) / int(source_image.size[0]))
        new_width = round(int(source_image.size[0]) * pan_results['zoom'], 0)
        new_height = round(int(source_image.size[1]) * pan_results['zoom'], 0)

        # calculate pan offset
        if pan_direction == 'N':
            self.settings['pan_y'] = round(self.settings['pan_y'] - round(new_height * 0.2, 0), 0)
        elif pan_direction == 'S':
            self.settings['pan_y'] = round(self.settings['pan_y'] + round(new_height * 0.2, 0), 0)
        elif pan_direction == 'E':
            self.settings['pan_x'] = round(self.settings['pan_x'] + round(new_width * 0.2, 0), 0)
        elif pan_direction == 'W':
            self.settings['pan_x'] = round(self.settings['pan_x'] - round(new_width * 0.2, 0), 0)
        elif pan_direction == 'NE':
            self.settings['pan_x'] = round(self.settings['pan_x'] + round(new_width * 0.2, 0), 0)
            self.settings['pan_y'] = round(self.settings['pan_y'] - round(new_height * 0.2, 0), 0)
        elif pan_direction == 'NW':
            self.settings['pan_x'] = round(self.settings['pan_x'] - round(new_width * 0.2, 0), 0)
            self.settings['pan_y'] = round(self.settings['pan_y'] - round(new_height * 0.2, 0), 0)
        elif pan_direction == 'SE':
            self.settings['pan_x'] = round(self.settings['pan_x'] + round(new_width * 0.2, 0), 0)
            self.settings['pan_y'] = round(self.settings['pan_y'] + round(new_height * 0.2, 0), 0)
        elif pan_direction == 'SW':
            self.settings['pan_x'] = round(self.settings['pan_x'] - round(new_width * 0.2, 0), 0)
            self.settings['pan_y'] = round(self.settings['pan_y'] + round(new_height * 0.2, 0), 0)
        elif pan_direction == 'C':
            self.settings['pan_x'] = 0
            self.settings['pan_y'] = 0

        # select the view region
        left = round((width - new_width) / 2, 0) + self.settings['pan_x']
        top = round((height - new_height) / 2, 0) + self.settings['pan_y']
        right = round((width + new_width) / 2, 0) + self.settings['pan_x']
        bottom = round((height + new_height) / 2, 0) + self.settings['pan_y']
        print('  z self.settings[pan_x] = ' + str(self.settings['pan_x']))
        print('  z self.settings[pan_y] = ' + str(self.settings['pan_y']))
        print('  z self.settings[zoom] = ' + str(self.settings['zoom']))

        # check for panning out of image area and adjust
        mid_x = round(int(source_image.size[0]) / 2)
        mid_y = round(int(source_image.size[1]) / 2)
        if left < 0:
            left = 0
            right = new_width
            self.settings['pan_x'] = mid_x - (int(source_image.size[0]) - round(new_width / 2, 0))
        elif right > int(source_image.size[0]):
            right = int(source_image.size[0])
            left = int(source_image.size[0]) - new_width
            self.settings['pan_x'] = mid_x - (int(source_image.size[0]) - round(new_width / 2, 0))

        if top < 0:
            top = 0
            bottom = new_height
            self.settings['pan_y'] = mid_y - (int(source_image.size[1]) - round(new_height / 2, 0))
        elif bottom > int(source_image.size[1]):
            bottom = int(source_image.size[1])
            top = int(source_image.size[1]) - new_height
            self.settings['pan_y'] = mid_y - round(new_height / 2, 0)

        print('  p self.settings[pan_x] = ' + str(self.settings['pan_x']))
        print('  p self.settings[pan_y] = ' + str(self.settings['pan_y']))
        print('  p self.settings[zoom] = ' + str(self.settings['zoom']))
        source_image = source_image.crop((int(left), int(top), int(right), int(bottom)))

        # What will we call this new image
        time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
        file_name, extension = os.path.splitext(current_image)
        output_file = 'tmp/zoom_' + time_stamp + extension
        source_image.save('static/' + output_file)
        pan_results['file'] = output_file
        return pan_results

    def info(self, pic_selected):
        image_info = Image.open(self.settings['path_to_pictures'] + '/' + pic_selected)
        pic_info = {
            'zoom_center_x': round(float(image_info.size[0]) / 2.0, 0),
            'zoom_center_y': round(float(image_info.size[1]) / 2.0, 0)}
        del image_info
        return pic_info

    def clean_tmp(self):
        delete_list = [f for f in listdir('static/tmp') if isfile(join('static/tmp', f))]
        for image in delete_list:
            filename_pieces = image.split('.')
            print('  removing ' + 'static/tmp/' + filename_pieces[0] + '.' + filename_pieces[1])
            os.remove('static/tmp/' + filename_pieces[0] + '.' + filename_pieces[1])
        return True

    def make_thumbnail(self, full_size_image):
        filename_pieces = full_size_image.split('/')
        print(str(filename_pieces))
