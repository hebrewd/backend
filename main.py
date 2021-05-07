from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/collect', methods = ['POST'])
def collect_data():
    data = request.form
    f = open("data.csv")
    f.write(data)
    f.close()

@app.route('/train', methods = ['POST'])
def train():
    os.system('python3 nns.py')

