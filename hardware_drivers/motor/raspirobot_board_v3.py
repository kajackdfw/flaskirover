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
