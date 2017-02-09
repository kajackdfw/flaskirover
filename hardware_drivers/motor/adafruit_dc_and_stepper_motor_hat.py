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
    try:
        mh = Adafruit_MotorHAT(addr=0x60)
        settings['drive'] = ''
    except NameError:
        print(" - No Adafruit_MotorHAT library available.")
        settings['drive'] = '-disabled'

    def __init__(self, start_settings):
        if 'drive_mode' in start_settings:
            self.settings['drive_mode'] = start_settings['drive_mode']
        else:
            self.settings['drive_mode'] = 'tank'

        if self.settings['drive_mode'] == 'tank':
            self.settings['can_rotate'] = True
        else:
            self.can_rotate_in_place = False

        if self.settings['drive'] == "":
            self.test(3)
            self.test(4)
            self.turnOffMotors()

    def forward_crawl(self, seconds):
        right_motor = self.mh.getMotor(3)
        left_motor = self.mh.getMotor(4)
        right_motor.setSpeed(25)
        left_motor.setSpeed(25)
        right_motor.run(Adafruit_MotorHAT.BACKWARD)
        left_motor.run(Adafruit_MotorHAT.BACKWARD)
        sleep(int(seconds))
        left_motor.setSpeed(0)
        right_motor.setSpeed(0)
        return True

    def backward_crawl(self, seconds):
        right_motor = self.mh.getMotor(3)
        left_motor = self.mh.getMotor(4)
        right_motor.setSpeed(25)
        left_motor.setSpeed(25)
        right_motor.run(Adafruit_MotorHAT.FORWARD)
        left_motor.run(Adafruit_MotorHAT.FORWARD)
        sleep(int(seconds))
        left_motor.setSpeed(0)
        right_motor.setSpeed(0)
        return True

    def rotate_ccw(self, seconds):
        right_motor = self.mh.getMotor(3)
        left_motor = self.mh.getMotor(4)
        right_motor.setSpeed(25)
        left_motor.setSpeed(25)
        right_motor.run(Adafruit_MotorHAT.BACKWARD)
        left_motor.run(Adafruit_MotorHAT.FORWARD)
        sleep(int(seconds))
        left_motor.setSpeed(0)
        right_motor.setSpeed(0)
        return True

    def rotate_cw(self, seconds):
        right_motor = self.mh.getMotor(3)
        left_motor = self.mh.getMotor(4)
        right_motor.setSpeed(25)
        left_motor.setSpeed(25)
        right_motor.run(Adafruit_MotorHAT.FORWARD)
        left_motor.run(Adafruit_MotorHAT.BACKWARD)
        sleep(int(seconds))
        left_motor.setSpeed(0)
        right_motor.setSpeed(0)
        return True

    # recommended for auto-disabling motors on shutdown!
    def turnOffMotors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    def test(self, motor_number):
        #self.atexit.register(turnOffMotors)
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
