
from flask import Flask, render_template
from DatabaseConnection import mongo_client
from datetime import datetime
import os

app = Flask(__name__)
IMAGE_PATH = 'https://campaign-banner-bucket.s3.us-west-2.amazonaws.com'

@app.route('/')
def index():
    return 'Hello World!'


@app.route('/<name>')
def print_name(name):
    return 'Hi, {}'.format(name)


@app.route('/banner/<banner_id>')
def banner_disp(banner_id):

    full_filename = IMAGE_PATH + "/image_{}.png".format(banner_id)
    print(full_filename)
    # return render_template("index.html", user_image = full_filename)
    return render_template("index.html", user_image = full_filename)


@app.route('/campaigns/<campaign_id>')
def handle_campaign(campaign_id):
    now = datetime.utcnow()
    if now.minute in range(0, 15):
        db_client = mongo_client.Quarter_1


        # get_all_click_id()


        pass
    elif now.minute in range(16, 30):

        pass
    elif now.minute in range(31, 45):
        pass
    elif now.minute in range(46, 60):
        pass


if __name__ == '__main__':
    app.run(debug=True)



