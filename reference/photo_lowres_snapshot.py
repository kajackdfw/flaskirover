from time import sleep
from picamera import PiCamera

# https://picamera.readthedocs.io/en/release-1.12/index.html
# https://www.raspberrypi.org/documentation/usage/camera/python/README.md
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture('foo.jpg', resize=(320, 240))