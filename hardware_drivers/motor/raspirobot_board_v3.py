from rrb3 import *
from time import sleep

class Motor:

    settings = {}

    try:
        rr = RRB3(8, 6)
        settings['drive'] = 'active'
        uis['drive'] = 'active'
    except NameError:
        print(" - No RaspiRover library available.")
        settings['drive'] = 'disabled'
        uis['drive'] = 'disabled'

    def __init__(self, start_settings):
        self.settings['motor_mode'] = 'immobile'
        self.can_rotate_in_place = False

    def test(self):
        track_right = 0.75
        track_left = 0.75
        rr.set_motors(track_right, 0.5, track_left, 0.5)
        sleep(2)
        rr.set_motors(0, 0.5, 0, 0.5)

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
