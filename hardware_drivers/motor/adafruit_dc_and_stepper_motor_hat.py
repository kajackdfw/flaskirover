import math
from os import listdir
from os.path import isfile, join
import os
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit
from time import sleep

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
        self.test()

    # recommended for auto-disabling motors on shutdown!
    def turnOffMotors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    def test(self):
        #self.atexit.register(turnOffMotors)
        myMotor = self.mh.getMotor(3)
        myMotor.setSpeed(150)
        while (True):
            print "Forward! "
            myMotor.run(Adafruit_MotorHAT.FORWARD)

            print "\tSpeed up..."
            for i in range(255):
                myMotor.setSpeed(i)
                sleep(0.01)

            print "\tSlow down..."
            for i in reversed(range(255)):
                myMotor.setSpeed(i)
                sleep(0.01)

            print "Backward! "
            myMotor.run(Adafruit_MotorHAT.BACKWARD)

            print "\tSpeed up..."
            for i in range(255):
                myMotor.setSpeed(i)
                sleep(0.01)

            print "\tSlow down..."
            for i in reversed(range(255)):
                myMotor.setSpeed(i)
                sleep(0.01)

            print "Release"
            myMotor.run(Adafruit_MotorHAT.RELEASE)
            sleep(1.0)
            exit()