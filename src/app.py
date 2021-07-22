
from flask import Flask
from DatabaseConnection import mongo_client

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/<name>')
def print_name(name):
    return 'Hi, {}'.format(name)


@app.route('/<banner_id>')
def print_name(banner_id):
    # Get banner from s3
    # Return banner in a proper format to FE.

    pass






if __name__ == '__main__':
    app.run()



