import math
from os import listdir
from os.path import isfile, join
import os
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit

class Motor:

    settings = {}
    mh = Adafruit_MotorHAT(addr=0x60)

    def __init__(self, start_settings):
        if 'drive_mode' in start_settings:
            self.settings['drive_mode'] = start_settings['drive_mode']
        else:
            self.settings['drive_mode'] = 'tank'

        if self.settings['drive_mode'] == 'tank':
            self.settings['can_rotate'] = True
        else:
            self.can_rotate_in_place = False
        self.settings['drive'] = '-disabled'

    # recommended for auto-disabling motors on shutdown!
    def turnOffMotors():
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


