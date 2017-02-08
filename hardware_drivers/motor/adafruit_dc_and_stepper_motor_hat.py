import math
from os import listdir
from os.path import isfile, join
import os

class Motor:

    settings = {}

    def __init__(self, start_settings):
        if 'drive_mode' in start_settings:
            self.settings['drive_mode'] = start_settings['drive_mode']
        else:
            self.settings['drive_mode'] = 'tank'

        if self.settings['drive_mode'] == 'tank':
            self.settings['can_rotate'] = True
        else:
            self.can_rotate_in_place = False
        self.settings['drive'] = '-disabled'
