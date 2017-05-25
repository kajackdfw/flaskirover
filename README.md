# FlaskiRover

***A Python Flask based Rover OS for the Raspberry PI***

**v0.03.01 WORKING**

1. Flask UI
2. Pi Camera
3. AdaFruit Motor Shield
4. UI Optimized for LG G4

**TESING OR IN DEVELOPMENT**

1. Build a settings page
1. Settings page for reversing or tweaking drive system 
1. Loadable hardware configs

**TODOS:**

1. RaspiRover Board v3 support
1. Load A User Created Config file for startup settings
1. Prompt User for setup and write a default config file
1. After a move into a wifi dead spot, reverse last move
1. Test wifi strength with download or normal drive page refresh

**FUTURE FEATURES:**
1. Link to Arduino by USB
1. Get sensor data from Arduino
1. Head lights
1. Nexus 7 UI Optimization
1. Arduino + Adafruit Motor Shield support
1. Camera Macro Support
1. Power Levels
1. 4G connection to cloud, instead of wifi/lan

**Raspberry Pi Install Dependencies** 

1. Python 3
1. sudo apt-get install python-dev
1. Pillow ( with pip3 )
1. Flask ( with pip3 )
1. WiringPi ( with pip3 )


**Windows**

_The windows setup is for UI development or demo only, Camera and Motor control on Raspberry Pi only._

1. Python 3
2. Flask

**Raspberry Pi Hardware Support**

1. AdaFruit Motor Hat ( https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/installing-software )
1. RaspiRobot v3 ( https://github.com/simonmonk/raspirobotboard3 )
1. Adafruit Servo Hat ( https://github.com/adafruit/Adafruit_Python_PCA9685 )

** Common I2C Addresses Used **

1. Adafruit Motor Hat --> 60
2. Adafruit Servo Hat --> 40
3. RaspiRobot         --> none ( uses GPIO ) ?
