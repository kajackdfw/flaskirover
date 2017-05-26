from __future__ import division
import time
try:
    import Adafruit_PCA9685
except ImportError:
    print(' - Library Adafruit_PCA9685 is not available on Windows.')


class Servo:

    settings = {}
    uis = {}
    pwm = False

    # Configure min and max servo pulse lengths
    servo_min = 150  # Min pulse length out of 4096
    servo_max = 600  # Max pulse length out of 4096

    try:
        pwm = Adafruit_PCA9685.PCA9685()
        # Alternatively specify a different address and/or bus:
        # pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

        pwm.set_pwm_freq(60)
        uis['servo_horz'] = 'active'
        uis['servo_vert'] = 'active'
    except NameError:
        print(" - No wiringpi library available.")
        uis['servo_vert'] = 'disabled'
        uis['servo_horz'] = 'disabled'

    def __init__(self, start_settings):
        self.settings['servo_camera_horz_number'] = start_settings['servo_camera_horz_number']
        self.settings['servo_camera_vert_number'] = start_settings['servo_camera_vert_number']

        if (self.settings['servo_camera_horz_number']) is not False and self.uis['servo_horz'] is not 'disabled':

            # wiringpi.pinMode(self.settings['servo_camera_horz_number'], wiringpi.GPIO.PWM_OUTPUT)
            self.settings['servo_camera_horz_number'] = int(self.settings['servo_camera_horz_number'])
            self.settings['servo_camera_horz_left'] = int(start_settings['servo_camera_horz_left'])
            self.settings['servo_camera_horz_center'] = int(start_settings['servo_camera_horz_center'])
            self.settings['servo_horz_position'] = int(start_settings['servo_camera_horz_center'])
            self.settings['servo_camera_horz_right'] = int(start_settings['servo_camera_horz_right'])
            self.settings['servo_camera_horz_inc'] = int(start_settings['servo_camera_horz_inc'])
        else:
            self.uis['servo_horz'] = 'disabled'

        if (self.settings['servo_camera_vert_number']) is not False and self.uis['servo_vert'] is not 'disabled':
            # wiringpi.pinMode(self.settings['servo_camera_vert_number'], wiringpi.GPIO.PWM_OUTPUT)
            self.settings['servo_camera_vert_number'] = int(self.settings['servo_camera_vert_number'])
            self.settings['servo_camera_vert_bottom'] = int(start_settings['servo_camera_vert_bottom'])
            self.settings['servo_camera_vert_center'] = int(start_settings['servo_camera_vert_center'])
            self.settings['servo_vert_position'] = int(start_settings['servo_camera_vert_center'])
            self.settings['servo_camera_vert_top'] = int(start_settings['servo_camera_vert_top'])
            self.settings['servo_camera_vert_inc'] = int(start_settings['servo_camera_vert_inc'])
        else:
            self.uis['servo_vert'] = 'disabled'

        # Initialize PWM and first servo positions
        if self.uis['servo_vert'] == 'active' or self.uis['servo_horz'] == 'active':
            # wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
            # wiringpi.pwmSetClock(192)
            # wiringpi.pwmSetRange(2000)
            self.center()

    def set_servo_pulse(self, channel, pulse):
        pulse_length = 1000000  # 1,000,000 us per second
        pulse_length //= 60  # 60 Hz
        print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096  # 12 bits of resolution
        print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        self.pwm.set_pwm(channel, 0, pulse)

    def center(self):
        if self.settings['servo_camera_vert_number'] is not False:
            self.pwm.set_pwm(self.settings['servo_camera_vert_number'], 0, self.settings['servo_camera_vert_center'])
        if self.settings['servo_camera_horz_number'] is not False:
            self.pwm.set_pwm(self.settings['servo_camera_horz_number'], 0, self.servo_min)
        return True

    def park(self):
        if self.settings['servo_camera_vert_number'] is not False:
            self.pwm.set_pwm(self.settings['servo_camera_vert_number'], 0, self.settings['servo_camera_vert_park'])
        if self.settings['servo_camera_horz_number'] is not False:
            self.pwm.set_pwm(0, 0, self.servo_min)
        return True

    def rotate_down(self, degrees):
        print(" ! rotate_down called")
        self.settings['servo_vert_position'] -= self.settings['servo_camera_vert_inc']
        #if self.settings['servo_vert_position'] < self.settings['servo_camera_vert_bottom']:
        #    self.settings['servo_vert_position'] = self.settings['servo_camera_vert_bottom']
        self.pwm.set_pwm(self.settings['servo_camera_vert_number'], 0, self.settings['servo_vert_position'])
        return True

    def rotate_up(self, degrees):
        print(" ! rotate_up called")
        self.settings['servo_vert_position'] += self.settings['servo_camera_vert_inc']
        #if self.settings['servo_vert_position'] > self.settings['servo_camera_vert_top']:
        #    self.settings['servo_vert_position'] = self.settings['servo_camera_vert_top']
        self.pwm.set_pwm(self.settings['servo_camera_vert_number'], 0, self.settings['servo_vert_position'])
        return True

    def rotate_left(self, degrees):
        self.settings['servo_horz_position'] += self.settings['servo_camera_horz_inc'] * int(degrees)
        if self.settings['servo_horz_position'] > self.settings['servo_camera_horz_left']:
            self.settings['servo_horz_position'] = self.settings['servo_camera_horz_left']
        # wiringpi.pwmWrite(self.settings['servo_camera_horz_number'], self.settings['servo_horz_position'])
        return False

    def rotate_right(self, degrees):
        self.settings['servo_horz_position'] -= self.settings['servo_camera_horz_inc'] * int(degrees)
        if self.settings['servo_horz_position'] > self.settings['servo_camera_horz_right']:
            self.settings['servo_horz_position'] = self.settings['servo_camera_horz_right']
        # wiringpi.pwmWrite(self.settings['servo_camera_horz_number'], self.settings['servo_horz_position'])
        return False

    def get_uis(self):
        return self.uis

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

