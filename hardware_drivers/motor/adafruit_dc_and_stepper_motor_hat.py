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
        else:
            self.can_rotate_in_place = False

        if self.settings['drive'] == "active":
            # self.test(3)
            # self.test(4)
            self.turn_off_motors()

    def forward_crawl(self, seconds):
        right_motor = self.mh.getMotor(self.settings['tank_right_motor'])
        left_motor = self.mh.getMotor(self.settings['tank_left_motor'])
        right_motor.setSpeed(self.settings['tank_speed_right'])
        left_motor.setSpeed(self.settings['tank_speed_left'])
        right_motor.run(self.settings['tank_right_forward'])
        left_motor.run(self.settings['tank_left_forward'])
        sleep(int(seconds))
        left_motor.setSpeed(0)
        right_motor.setSpeed(0)
        return True

    def backward_crawl(self, seconds):
        right_motor = self.mh.getMotor(self.settings['tank_right_motor'])
        left_motor = self.mh.getMotor(self.settings['tank_left_motor'])
        right_motor.setSpeed(self.settings['tank_speed_right'])
        left_motor.setSpeed(self.settings['tank_speed_left'])
        right_motor.run(self.settings['tank_right_reverse'])
        left_motor.run(self.settings['tank_left_reverse'])
        sleep(int(seconds))
        left_motor.setSpeed(0)
        right_motor.setSpeed(0)
        return True

    def rotate_ccw(self, second_hundredths):
        right_motor = self.mh.getMotor(self.settings['tank_right_motor'])
        left_motor = self.mh.getMotor(self.settings['tank_left_motor'])
        right_motor.setSpeed(self.settings['tank_turn_speed'])
        left_motor.setSpeed(self.settings['tank_turn_speed'])
        right_motor.run(self.settings['tank_right_forward'])
        left_motor.run(self.settings['tank_left_reverse'])
        sleep(float(second_hundredths) / 100)
        left_motor.setSpeed(0)
        right_motor.setSpeed(0)
        return True

    def rotate_cw(self, second_hundredths):
        right_motor = self.mh.getMotor(self.settings['tank_right_motor'])
        left_motor = self.mh.getMotor(self.settings['tank_left_motor'])
        right_motor.setSpeed(self.settings['tank_turn_speed'])
        left_motor.setSpeed(self.settings['tank_turn_speed'])
        right_motor.run(self.settings['tank_right_reverse'])
        left_motor.run(self.settings['tank_left_forward'])
        sleep(float(second_hundredths) / 100)
        left_motor.setSpeed(0)
        right_motor.setSpeed(0)
        return True

    # recommended for auto-disabling motors on shutdown!
    def turn_off_motors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    def test(self, motor_number):
        # self.atexit.register(turn_off_motors)
        myMotor = self.mh.getMotor(motor_number)
        myMotor.setSpeed(75)
        while (True):
            print("Forward! ")
            myMotor.run(Adafruit_MotorHAT.FORWARD)

            print("\tSpeed up...")
            for i in range(255):
                myMotor.setSpeed(i)
                sleep(0.01)

            print("\tSlow down...")
            for i in reversed(range(255)):
                myMotor.setSpeed(i)
                sleep(0.01)

            print("Backward! ")
            myMotor.run(Adafruit_MotorHAT.BACKWARD)

            print("\tSpeed up...")
            for i in range(255):
                myMotor.setSpeed(i)
                sleep(0.01)

            print("\tSlow down...")
            for i in reversed(range(255)):
                myMotor.setSpeed(i)
                sleep(0.01)

            print("Release")
            myMotor.run(Adafruit_MotorHAT.RELEASE)
            sleep(1.0)
            return True

    def get_uis(self):
        return self.uis