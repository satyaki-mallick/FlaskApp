
from flask import Flask, render_template
from database import mongo_client
from datetime import datetime
import database
import os
from pprint import pprint

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


@app.route('/campaigns/<id>')
def handle_campaign(id):
    now = datetime.utcnow()
    campaign_id = int(id)
    if now.minute in range(0, 60):  # TODO: Change after testing
        db_client = mongo_client.Quarter_1  # TODO: Test DB. Change before publish

        X = fetch_all_banners_for_campaign(db_client, campaign_id)

        handle_no_of_banners(X)

        return 'Hello World!'

    elif now.minute in range(16, 30):

        pass
    elif now.minute in range(31, 45):
        pass
    elif now.minute in range(46, 60):
        pass

    mongo_client.close()


def fetch_all_banners_for_campaign(db_client, campaign_id):
    conversions_collection = db_client.conversions_1
    clicks_collection = db_client.clicks_1
    conversions = conversions_collection.find().sort([("revenue", -1)])
    clicks = clicks_collection.find({"campaign_id": campaign_id})

    my_dict = {}
    banner_revenue_list = []

    for item in clicks:
        key = item['click_id']
        my_dict[key] = item

    pprint(my_dict)
    for item in conversions:

        key = item['click_id']
        print('conversion_click_id' + str(key))
        revenue = item['revenue']
        print('revenue' + str(revenue))
        if key in my_dict.keys():
            val = my_dict[key]
            tup = val['banner_id'], revenue
            banner_revenue_list.append(tup)

    print("Full Tuple " + str(banner_revenue_list))
    return tup


def handle_no_of_banners(X):
    pass



if __name__ == '__main__':
    app.run(debug=True)



