try:
    import RPi.GPIO as GPIO
except ImportError:
    print(' - Library Rpi GPIO is not available on Windows.')

class Gimbal:

    settings = {}
    uis = {}
    pwm_horz = False
    pwm_vert = False

    try:
        GPIO.setmode(GPIO.BOARD)
        uis['gimbal_horz'] = 'active'
        uis['gimbal_vert'] = 'active'
    except NameError:
        print(" - No Rpi GPIO library available.")
        settings['gimbal_horz_servo_gpio'] = False
        settings['gimbal_vert_servo_gpio'] = False
        uis['gimbal_vert'] = 'disabled'
        uis['gimbal_horz'] = 'disabled'

    def __init__(self, start_settings):
        self.settings['gimbal_horz_servo_gpio'] = start_settings['gimbal_horz_servo_gpio']
        self.settings['gimbal_vert_servo_gpio'] = start_settings['gimbal_vert_servo_gpio']

        if (self.settings['gimbal_horz_servo_gpio']) is not False:
            self.settings['gimbal_horz_full_left'] = start_settings['gimbal_horz_full_left']
            self.settings['gimbal_horz_center'] = start_settings['gimbal_horz_center']
            self.settings['gimbal_horz_full_right'] = start_settings['gimbal_horz_full_right']
            self.settings['gimbal_horz_step'] = start_settings['gimbal_horz_step']
        else:
            self.uis['gimbal_horz'] = 'disabled'

        if (self.settings['gimbal_vert_servo_gpio']) is not False:
            self.settings['gimbal_vert_full_down'] = start_settings['gimbal_vert_full_down']
            self.settings['gimbal_vert_center'] = start_settings['gimbal_vert_center']
            self.settings['gimbal_vert_full_up'] = start_settings['gimbal_vert_full_up']
            self.settings['gimbal_vert_step'] = start_settings['gimbal_vert_step']
        else:
            self.uis['gimbal_vert'] = 'disabled'

        # Initialize servos
        if self.settings['gimbal_vert_servo_gpio'] and self.uis['gimbal_vert'] == 'active':
            GPIO.setup(self.settings['gimbal_vert_servo_gpio'], GPIO.OUT)
            self.pwm_vert = GPIO.PWM(self.settings['gimbal_vert_servo_gpio'], 50)
            self.pwm_vert.start(5)
            self.center()

        if self.settings['gimbal_horz_servo_gpio'] and self.uis['gimbal_horz'] == 'active':
            GPIO.setup(self.settings['gimbal_horz_servo_gpio'], GPIO.OUT)
            self.pwm_horz= GPIO.PWM(self.settings['gimbal_horz_servo_gpio'], 50)
            self.pwm_horz.start(5)
            self.center()

    def center(self):
        if self.settings['gimbal_vert_servo_gpio']:
            self.pwm_vert.ChangeDutyCycle(7.5)
        if self.settings['gimbal_horz_servo_gpio']:
            self.pwm_horz.ChangeDutyCycle(7.5)
        return True

    def rotate_down(self, degrees):
        self.pwm_vert.ChangeDutyCycle(7)

    def rotate_up(self, degrees):
        self.pwm_vert.ChangeDutyCycle(8)

    def rotate_left(self, degrees):
        self.pwm_horz.ChangeDutyCycle(7)

    def rotate_right(self, degrees):
        self.pwm_horz.ChangeDutyCycle(8)

    def get_uis(self):
        return self.uis
