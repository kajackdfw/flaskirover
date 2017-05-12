try:
    import wiringpi
except ImportError:
    print(' - Library wiringpi is not available on Windows.')


class Gimbal:

    settings = {}
    uis = {}
    pwm_horz = False
    pwm_vert = False

    try:
        wiringpi.wiringPiSetupGpio()
        delay_period = 0.01
        uis['gimbal_horz'] = 'active'
        uis['gimbal_vert'] = 'active'
    except NameError:
        print(" - No wiringpi library available.")
        uis['gimbal_vert'] = 'disabled'
        uis['gimbal_horz'] = 'disabled'

    def __init__(self, start_settings):
        self.settings['gimbal_horz_servo_gpio'] = start_settings['gimbal_horz_servo_gpio']
        self.settings['gimbal_vert_servo_gpio'] = start_settings['gimbal_vert_servo_gpio']

        if (self.settings['gimbal_horz_servo_gpio']) is not False and self.uis['gimbal_horz'] is not 'disabled':
            wiringpi.pinMode(self.settings['gimbal_horz_servo_gpio'], wiringpi.GPIO.PWM_OUTPUT)
            self.settings['gimbal_horz_servo_gpio'] = int(self.settings['gimbal_horz_servo_gpio'])
            self.settings['gimbal_horz_full_left'] = int(start_settings['gimbal_horz_full_left'])
            self.settings['gimbal_horz_center'] = int(start_settings['gimbal_horz_center'])
            self.settings['gimbal_horz_position'] = int(start_settings['gimbal_horz_center'])
            self.settings['gimbal_horz_full_right'] = int(start_settings['gimbal_horz_full_right'])
            self.settings['gimbal_horz_step'] = int(start_settings['gimbal_horz_step'])
        else:
            self.uis['gimbal_horz'] = 'disabled'

        if (self.settings['gimbal_vert_servo_gpio']) is not False and self.uis['gimbal_vert'] is not 'disabled':
            wiringpi.pinMode(self.settings['gimbal_vert_servo_gpio'], wiringpi.GPIO.PWM_OUTPUT)

            self.settings['gimbal_vert_servo_gpio'] = int(self.settings['gimbal_vert_servo_gpio'])
            self.settings['gimbal_vert_full_down'] = int(start_settings['gimbal_vert_full_down'])
            self.settings['gimbal_vert_center'] = int(start_settings['gimbal_vert_center'])
            self.settings['gimbal_vert_position'] = int(start_settings['gimbal_vert_center'])
            self.settings['gimbal_vert_full_up'] = int(start_settings['gimbal_vert_full_up'])
            self.settings['gimbal_vert_step'] = int(start_settings['gimbal_vert_step'])
        else:
            self.uis['gimbal_vert'] = 'disabled'

        # Initialize PWM and first servo positions
        if self.uis['gimbal_vert'] == 'active' or self.uis['gimbal_horz'] == 'active':
            wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
            wiringpi.pwmSetClock(192)
            wiringpi.pwmSetRange(2000)
            self.center()

    def center(self):
        if self.settings['gimbal_vert_servo_gpio'] is not False:
            wiringpi.pwmWrite(self.settings['gimbal_vert_servo_gpio'], self.settings['gimbal_vert_center'])

        if self.settings['gimbal_horz_servo_gpio'] is not False:
            wiringpi.pwmWrite(self.settings['gimbal_horz_servo_gpio'], self.settings['gimbal_horz_center'])

        return True

    def rotate_down(self, degrees):
        self.settings['gimbal_vert_position'] -= self.settings['gimbal_vert_step'] * int(degrees)
        if self.settings['gimbal_vert_position'] < self.settings['gimbal_vert_full_down']:
            self.settings['gimbal_vert_position'] = self.settings['gimbal_vert_full_down']
        wiringpi.pwmWrite(self.settings['gimbal_vert_servo_gpio'], self.settings['gimbal_vert_position'])
        return False

    def rotate_up(self, degrees):
        self.settings['gimbal_vert_position'] += self.settings['gimbal_vert_step'] * int(degrees)
        if self.settings['gimbal_vert_position'] > self.settings['gimbal_vert_full_up']:
            self.settings['gimbal_vert_position'] = self.settings['gimbal_vert_full_up']
        wiringpi.pwmWrite(self.settings['gimbal_vert_servo_gpio'], self.settings['gimbal_vert_position'])
        return False

    def rotate_left(self, degrees):
        self.settings['gimbal_horz_position'] += self.settings['gimbal_horz_step'] * int(degrees)
        if self.settings['gimbal_horz_position'] > self.settings['gimbal_horz_full_left']:
            self.settings['gimbal_horz_position'] = self.settings['gimbal_horz_full_left']
        wiringpi.pwmWrite(self.settings['gimbal_horz_servo_gpio'], self.settings['gimbal_horz_position'])
        return False

    def rotate_right(self, degrees):
        self.settings['gimbal_horz_position'] -= self.settings['gimbal_horz_step'] * int(degrees)
        if self.settings['gimbal_horz_position'] > self.settings['gimbal_horz_full_right']:
            self.settings['gimbal_horz_position'] = self.settings['gimbal_horz_full_right']
        wiringpi.pwmWrite(self.settings['gimbal_horz_servo_gpio'], self.settings['gimbal_horz_position'])
        return False

    def get_uis(self):
        return self.uis
