import random

from flask import Flask, render_template
from database import mongo_client
from datetime import datetime
import database
import os
from pprint import pprint
import random

app = Flask(__name__)
IMAGE_PATH = 'https://campaign-banner-bucket.s3.us-west-2.amazonaws.com'

@app.route('/')
def index():
    return 'Hello World!'


@app.route('/<name>')
def print_name(name):
    return 'Hi, {}'.format(name)


@app.route('/test/<banner_id>')
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

        banners_to_display = handle_no_of_banners(X)
        # Padding list with zeroes
        banners_to_display += [0] * (10 - len(banners_to_display))

        filename0 = IMAGE_PATH + "/image_{}.png".format(banners_to_display[0])
        filename1 = IMAGE_PATH + "/image_{}.png".format(banners_to_display[1])
        filename2 = IMAGE_PATH + "/image_{}.png".format(banners_to_display[2])
        filename3 = IMAGE_PATH + "/image_{}.png".format(banners_to_display[3])
        filename4 = IMAGE_PATH + "/image_{}.png".format(banners_to_display[4])

        filename5 = IMAGE_PATH + "/image_{}.png".format(banners_to_display[5])
        filename6 = IMAGE_PATH + "/image_{}.png".format(banners_to_display[6])
        filename7 = IMAGE_PATH + "/image_{}.png".format(banners_to_display[7])
        filename8 = IMAGE_PATH + "/image_{}.png".format(banners_to_display[8])
        filename9 = IMAGE_PATH + "/image_{}.png".format(banners_to_display[9])


        return render_template("index.html", image0 = filename0,
                               image1 = filename1,
                               image2 = filename2,
                               image3 = filename3,
                               image4 = filename4,

                               image5 = filename5,
                               image6 = filename6,
                               image7 = filename7,
                               image8 = filename8,
                               image9 = filename9,
                               )

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

    for item in conversions:

        key = item['click_id']
        revenue = item['revenue']
        if key in my_dict.keys():
            val = my_dict[key]
            tup = val['banner_id'], revenue
            banner_revenue_list.append(tup)

    return banner_revenue_list


def handle_no_of_banners(X):
    if len(X) >= 10:
        top_10 = X[:10]
        random.shuffle(top_10)

        banner_ids = [item[0] for item in top_10]

        return banner_ids

    elif len(X) in range(5,10):
        top_X = X[:len(X)]
        random.shuffle(top_X)

        return top_X

    elif len(X) in range(1,5):
        top_X = X[:len(X)]
        random.shuffle(top_X)

        banners_remain = 5 - len(X)
        # TODO: Find these many banners with most clicks
        # Append to top_X
        # Return top_X

        pass
    else:
        # TODO: Show top 5 banners based on clicks
        # If this is less than 5
        # Add random banners to it

        pass
    pass


if __name__ == '__main__':
    app.run(debug=True)



