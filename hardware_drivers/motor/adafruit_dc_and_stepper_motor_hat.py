import math
from os import listdir
from os.path import isfile, join
import os

try:
    from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
except ImportError:
    print(' - Library Adafruit_MotorHAT not installed.')

import time
import atexit
from time import sleep

class Motor:

    settings = {}
    uis = {}

    try:
        mh = Adafruit_MotorHAT(addr=0x60)
        settings['drive'] = 'active'
        uis['drive'] = 'active'
        uis['motor_speed'] = 1.0
        right_motor = None
        left_motor = None
    except NameError:
        print(" - No Adafruit_MotorHAT library available.")
        settings['drive'] = 'disabled'
        uis['drive'] = 'disabled'
        uis['motor_speed'] = 1.0

    def __init__(self, start_settings):

        if self.uis['drive'] == 'disabled':
            return None

        if 'motor_mode' in start_settings:
            self.settings['motor_mode'] = start_settings['motor_mode']
        else:
            self.settings['motor_mode'] = 'tank'

        if self.settings['motor_mode'] == 'tank':
            for setting, value in start_settings.items():
                if setting[0:4] == 'tank':
                    self.settings[setting] = int(value)
            self.right_motor = self.mh.getMotor(self.settings['tank_right_motor'])
            self.left_motor = self.mh.getMotor(self.settings['tank_left_motor'])
        else:
            self.can_rotate_in_place = False

        if self.settings['drive'] == "active":
            # self.test(3)
            # self.test(4)
            self.turn_off_motors()
            self.settings['motor_speed'] = 1.0

    def speed_adjust(self, multiplier):
        self.settings['motor_speed'] = float(multiplier)
        self.uis['motor_speed'] = float(multiplier)
        return True

    def forward_crawl(self, seconds):
        if self.settings['motor_speed'] == 2.0:
            self.right_motor.setSpeed(self.settings['tank_speed_right_max'])
            self.left_motor.setSpeed(self.settings['tank_speed_left_max'])
        else:
            self.right_motor.setSpeed(int(self.settings['tank_speed_right'] * self.settings['motor_speed']))
            self.left_motor.setSpeed(int(self.settings['tank_speed_left'] * self.settings['motor_speed']))

        self.right_motor.run(self.settings['tank_right_forward'])
        self.left_motor.run(self.settings['tank_left_forward'])
        sleep(int(seconds))
        self.left_motor.setSpeed(0)
        self.right_motor.setSpeed(0)
        return True

    def backward_crawl(self, seconds):
        if self.settings['motor_speed'] == 2.0:
            self.right_motor.setSpeed(self.settings['tank_speed_right_max'])
            self.left_motor.setSpeed(self.settings['tank_speed_left_max'])
        else:
            self.right_motor.setSpeed(int(self.settings['tank_speed_right'] * self.settings['motor_speed']))
            self.left_motor.setSpeed(int(self.settings['tank_speed_left'] * self.settings['motor_speed']))

        self.right_motor.run(self.settings['tank_right_reverse'])
        self.left_motor.run(self.settings['tank_left_reverse'])
        sleep(int(seconds))
        self.left_motor.setSpeed(0)
        self.right_motor.setSpeed(0)
        return True

    def rotate_ccw(self, second_hundredths):
        if self.settings['motor_speed'] == 2.0:
            self.right_motor.setSpeed(self.settings['tank_speed_right_max'])
            self.left_motor.setSpeed(self.settings['tank_speed_left_max'])
        else:
            self.right_motor.setSpeed(int(self.settings['tank_speed_right'] * self.settings['motor_speed']))
            self.left_motor.setSpeed(int(self.settings['tank_speed_left'] * self.settings['motor_speed']))

        self.right_motor.run(self.settings['tank_right_forward'])
        self.left_motor.run(self.settings['tank_left_reverse'])
        sleep(float(second_hundredths) / 100)
        self.left_motor.setSpeed(0)
        self.right_motor.setSpeed(0)
        return True

    def rotate_cw(self, second_hundredths):
        if self.settings['motor_speed'] == 2.0:
            self.right_motor.setSpeed(self.settings['tank_speed_right_max'])
            self.left_motor.setSpeed(self.settings['tank_speed_left_max'])
        else:
            self.right_motor.setSpeed(int(self.settings['tank_speed_right'] * self.settings['motor_speed']))
            self.left_motor.setSpeed(int(self.settings['tank_speed_left'] * self.settings['motor_speed']))

        self.right_motor.run(self.settings['tank_right_reverse'])
        self.left_motor.run(self.settings['tank_left_forward'])
        sleep(float(second_hundredths) / 100)
        self.left_motor.setSpeed(0)
        self.right_motor.setSpeed(0)
        return True

    # recommended for auto-disabling motors on shutdown!
    def turn_off_motors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

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