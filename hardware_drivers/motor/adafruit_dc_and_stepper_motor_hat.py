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
        right_motor = None
        left_motor = None
    except NameError:
        print(" - No Adafruit_MotorHAT library available.")
        settings['drive'] = 'disabled'
        uis['drive'] = 'disabled'

    def __init__(self, start_settings):

        if self.uis['drive'] == 'disabled':
            return None

        if 'drive_mode' in start_settings:
            self.settings['drive_mode'] = start_settings['drive_mode']
        else:
            self.settings['drive_mode'] = 'tank'

        if self.settings['drive_mode'] == 'tank':
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
        return True

    def forward_crawl(self, seconds):
        if self.settings['motor_speed'] == 1.0:
            self.right_motor.run(self.settings['tank_right_forward'])
            self.left_motor.run(self.settings['tank_left_forward'])
        elif self.settings['motor_speed'] == 1.5:
            self.right_motor.run(int(self.settings['tank_right_forward'] * 1.5))
            self.left_motor.run(int(self.settings['tank_left_forward'] * 1.5))
        elif self.settings['motor_speed'] == 0.75:
            self.right_motor.run(int(self.settings['tank_right_forward'] * 0.75))
            self.left_motor.run(int(self.settings['tank_left_forward'] * 0.75))
        elif self.settings['motor_speed'] == 2.0:
            self.right_motor.run(int(self.settings['tank_speed_right_max'] * 0.75))
            self.left_motor.run(int(self.settings['tank_speed_left_max'] * 0.75))

        sleep(int(seconds))
        self.left_motor.setSpeed(0)
        self.right_motor.setSpeed(0)
        return True

    def backward_crawl(self, seconds):
        # right_motor = self.mh.getMotor(self.settings['tank_right_motor'])
        # left_motor = self.mh.getMotor(self.settings['tank_left_motor'])
        self.right_motor.setSpeed(self.settings['tank_speed_right'])
        self.left_motor.setSpeed(self.settings['tank_speed_left'])
        self.right_motor.run(self.settings['tank_right_reverse'])
        self.left_motor.run(self.settings['tank_left_reverse'])
        sleep(int(seconds))
        self.left_motor.setSpeed(0)
        self.right_motor.setSpeed(0)
        return True

    def rotate_ccw(self, second_hundredths):
        # right_motor = self.mh.getMotor(self.settings['tank_right_motor'])
        # left_motor = self.mh.getMotor(self.settings['tank_left_motor'])
        self.right_motor.setSpeed(self.settings['tank_turn_speed'])
        self.left_motor.setSpeed(self.settings['tank_turn_speed'])
        self.right_motor.run(self.settings['tank_right_forward'])
        self.left_motor.run(self.settings['tank_left_reverse'])
        sleep(float(second_hundredths) / 100)
        self.left_motor.setSpeed(0)
        self.right_motor.setSpeed(0)
        return True

    def rotate_cw(self, second_hundredths):
        # right_motor = self.mh.getMotor(self.settings['tank_right_motor'])
        # left_motor = self.mh.getMotor(self.settings['tank_left_motor'])
        self.right_motor.setSpeed(self.settings['tank_turn_speed'])
        self.left_motor.setSpeed(self.settings['tank_turn_speed'])
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