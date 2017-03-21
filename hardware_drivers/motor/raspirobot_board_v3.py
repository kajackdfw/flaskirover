# no motors, this is a stationary rover or wildlife cam


class Motor:

    settings = {}

    def __init__(self, start_settings):
        self.settings['drive_mode'] = 'immobile'
        self.can_rotate_in_place = False
