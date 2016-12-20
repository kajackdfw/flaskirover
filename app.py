from flask import Flask, render_template
from os import listdir
from os.path import isfile, join
import os

app = Flask(__name__)
server_os = os.name
if os.name == 'nt':
    mypath = 'static/webcam'  # 'C:/Users/kajac/Documents/Projects_Python/raspberry_flask_garden/static/webcam'
else:
    mypath = 'static/webcam'

@app.route('/')
def index():
    # mypath = 'static/webcam'
    imagefiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return render_template('index.html', images=imagefiles)

@app.route('/view/<image>')
def view(image):
    return render_template('view.html', image=image)

@app.route('/drive')
def drive():
    imagefiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return render_template('drive.html', images=imagefiles)

if __name__ == '__main__' and os.name == 'posix':
    app.run(debug=True, host='0.0.0.0')
elif __name__ == '__main__':
    app.run(debug=True, host='localhost')
