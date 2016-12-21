from flask import Flask, render_template
from os import listdir
from os.path import isfile, join
import os
from flaskenrover import Rover

app = Flask(__name__)
server_os = os.name
startup_settings = {}

if os.path.isdir('static/webcam'):
    startup_settings['path_to_web_cam'] = 'static/webcam'
    startup_settings['path_to_pictures'] = 'static/camera/photos'
    startup_settings['path_to_thumbnails'] = 'static/camera/thumbnails'
else:
    startup_settings['path_to_web_cam'] = '/tmp/static/webcam'
    startup_settings['path_to_pictures'] = '/tmp/static/camera/photos'
    startup_settings['path_to_thumbnails'] = '/tmp/static/camera/thumbnails'

# Plugin the hardware driver classes here
vision = Rover(startup_settings)
motor = Rover(startup_settings)

@app.route('/')
def index():
    # path_to_webcam = 'static/webcam'
    imagefiles = [f for f in listdir(startup_settings['path_to_thumbnails']) if isfile(join(startup_settings['path_to_thumbnails'], f))]
    return render_template('index.html', images=imagefiles, path=startup_settings['path_to_thumbnails'])


@app.route('/view/<image>')
def view(image):
    return render_template('view.html', image=image)


@app.route('/drive')
def drive():
    latest_image = vision.get_latest_web_cam_image()
    return render_template('drive.html', image=latest_image)

if __name__ == '__main__' and os.name == 'posix':
    app.run(debug=True, host='0.0.0.0')
elif __name__ == '__main__':
    app.run(debug=True, host='localhost')

