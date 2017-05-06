try:
    import RPi.GPIO as GPIO
except ImportError:
    print(' - Library Rpi GPIO is not available on Windows.')

class Gimbal:

    settings = {}
    uis = {}

    try:
        GPIO.setmode(GPIO.BOARD)
        uis['gimbal_horz'] = 'active'
        uis['gimbal_vert'] = 'active'
    except NameError:
        print(" - No Rpi GPIO library available.")
        settings['gimbal_horz'] = 'False'
        uis['gimbal_horz'] = 'disabled'
        settings['gimbal_vert'] = 'False'
        uis['gimbal_vert'] = 'disabled'

    def __init__(self, start_settings):
        self.settings['gimbal_horz_servo_gpio'] = start_settings['gimbal_horz_servo_gpio']
        self.settings['gimbal_vert_servo_gpio'] = start_settings['gimbal_vert_servo_gpio']

        if (self.settings['gimbal_horz_servo_gpio']) is not False:
            self.settings['gimbal_horz_full_left'] = start_settings['gimbal_horz_full_left']
            self.settings['gimbal_horz_center'] = start_settings['gimbal_horz_center']
            self.settings['gimbal_horz_full_right'] = start_settings['gimbal_horz_full_right']
            self.settings['gimbal_horz_step'] = start_settings['gimbal_horz_step']
            self.uis['gimbal_horz'] = 'active'
        else:
            self.uis['gimbal_horz'] = 'disabled'

        if (self.settings['gimbal_vert_servo_gpio']) is not False:
            self.settings['gimbal_vert_full_down'] = start_settings['gimbal_vert_full_down']
            self.settings['gimbal_vert_center'] = start_settings['gimbal_vert_center']
            self.settings['gimbal_vert_full_up'] = start_settings['gimbal_vert_full_up']
            self.settings['gimbal_vert_step'] = start_settings['gimbal_vert_step']
            self.uis['gimbal_vert'] = 'active'
        else:
            self.uis['gimbal_vert'] = 'disabled'

    def get_uis(self):
        return self.uis