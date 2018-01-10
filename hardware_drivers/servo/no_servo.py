from __future__ import division


class Servo:

    settings = {}
    uis = {}

    position = {}
    position['horz'] = 0
    position['vert'] = 0

    # Configure min and max servo pulse lengths
    uis['servo_vert'] = 'disabled'
    uis['servo_horz'] = 'disabled'

    def __init__(self, start_settings):
        self.settings['servo_camera_horz_number'] = -1
        self.settings['servo_camera_vert_number'] = -1

    def get_uis(self):
        return self.uis

    def get_settings(self):
        return self.settings
