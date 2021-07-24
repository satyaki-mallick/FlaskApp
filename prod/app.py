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
    return render_template("scratch.html", user_image=full_filename)


@app.route('/campaign/<some_id>')
def handle_campaign(some_id):
    now = datetime.utcnow()
    campaign_id = int(some_id)

    if campaign_id not in range(1, 51):
        return "Campaign does not exist", 400

    db_client = mongo_client.MyFirstDatabase
    banners_worthy_of_display = []
    if now.minute in range(0, 15):
        print('Executing Quarter1 code block')

        x_banners, banner_click_counter = fetch_all_banners_for_given_campaign(db_client, campaign_id , 1)
        banners_worthy_of_display = render_banners_for_display(x_banners, banner_click_counter)

    elif now.minute in range(15, 30):
        print('Executing Quarter2 code block')

        x_banners, banner_click_counter = fetch_all_banners_for_given_campaign(db_client, campaign_id , 2)
        banners_worthy_of_display = render_banners_for_display(x_banners, banner_click_counter)

    elif now.minute in range(30, 45):
        print('Executing Quarter3 code block')
        x_banners, banner_click_counter = fetch_all_banners_for_given_campaign(db_client, campaign_id , 3)
        banners_worthy_of_display = render_banners_for_display(x_banners, banner_click_counter)

    elif now.minute in range(45, 60):
        print('Executing Quarter4 code block')

        x_banners, banner_click_counter = fetch_all_banners_for_given_campaign(db_client, campaign_id , 4)
        banners_worthy_of_display = render_banners_for_display(x_banners, banner_click_counter)

    mongo_client.close()

    # Padding list with zeroes
    banners_worthy_of_display += [0] * (10 - len(banners_worthy_of_display))

    filename0 = IMAGE_PATH + "/image_{}.png".format(banners_worthy_of_display[0])
    filename1 = IMAGE_PATH + "/image_{}.png".format(banners_worthy_of_display[1])
    filename2 = IMAGE_PATH + "/image_{}.png".format(banners_worthy_of_display[2])
    filename3 = IMAGE_PATH + "/image_{}.png".format(banners_worthy_of_display[3])
    filename4 = IMAGE_PATH + "/image_{}.png".format(banners_worthy_of_display[4])

    filename5 = IMAGE_PATH + "/image_{}.png".format(banners_worthy_of_display[5])
    filename6 = IMAGE_PATH + "/image_{}.png".format(banners_worthy_of_display[6])
    filename7 = IMAGE_PATH + "/image_{}.png".format(banners_worthy_of_display[7])
    filename8 = IMAGE_PATH + "/image_{}.png".format(banners_worthy_of_display[8])
    filename9 = IMAGE_PATH + "/image_{}.png".format(banners_worthy_of_display[9])

    return render_template("index.html", image0=filename0,
                           image1=filename1,
                           image2=filename2,
                           image3=filename3,
                           image4=filename4,

                           image5=filename5,
                           image6=filename6,
                           image7=filename7,
                           image8=filename8,
                           image9=filename9,
                           ), 200


def fetch_all_banners_for_given_campaign(db_client, campaign_id, time_id):

    conversions_id = 'conversions_' + str(time_id)
    clicks_id = 'clicks_' + str(time_id)
    conversions_collection = db_client[conversions_id]
    clicks_collection = db_client[clicks_id]
    conversions = conversions_collection.find().sort([("revenue", -1)])
    clicks = clicks_collection.find({"campaign_id": campaign_id})

    click_hash_table = {}
    banners_ordered_by_revenue = []
    banner_click_counter = {}

    for item in clicks:
        key = item['click_id']
        click_hash_table[key] = item

        key = item['banner_id']
        if key in banner_click_counter:
            banner_click_counter[key] += 1
        else:
            banner_click_counter[key] = 1

    for item in conversions:

        click_that_converted = item['click_id']
        if click_that_converted in click_hash_table.keys():
            corresponding_details = click_hash_table[click_that_converted]
            banner_of_the_converted_click = corresponding_details['banner_id']
            banners_ordered_by_revenue.append(banner_of_the_converted_click)

    print("banners_ordered_by_revenue" + str(banners_ordered_by_revenue))
    return banners_ordered_by_revenue, banner_click_counter


def render_banners_for_display(banners_ordered_by_revenue, banner_click_counter):
    if len(banners_ordered_by_revenue) >= 10:

        print('Banners by Revenue >= 10')
        top_10_grossing = banners_ordered_by_revenue[:10]
        random.shuffle(top_10_grossing)

        return top_10_grossing
        # For DEBUG mode
        # find_banners_with_most_clicks(banner_click_counter, 3)

    elif len(banners_ordered_by_revenue) in range(5, 10):

        print('Banners by Revenue X: 5 <= X < 10')
        top_grossing = banners_ordered_by_revenue.copy()
        random.shuffle(top_grossing)

        return top_grossing

    elif len(banners_ordered_by_revenue) in range(1, 5):

        print('Banners by Revenue X: 1 <= X < 5')
        top_grossing = banners_ordered_by_revenue.copy()
        remaining_banners_to_display = 5 - len(top_grossing)
        find_banners_with_most_clicks(banner_click_counter, remaining_banners_to_display, top_grossing)

        random.shuffle(top_grossing)
        return top_grossing

    else:

        print('Banners by Revenue X: X=0')
        top_grossing = []
        find_banners_with_most_clicks(banner_click_counter, 5, top_grossing)
        random.shuffle(top_grossing)
        return top_grossing

    pass


def find_banners_with_most_clicks(banner_click_counter, banners_remain, top_grossing):

    new_banners = []
    use_length = min(len(banner_click_counter), banners_remain)

    for i in range(use_length):
        key = max(banner_click_counter, key=banner_click_counter.get)
        new_banners.append(key)

        banner_click_counter.pop(key)

    # Append random banners if enough most clicked banners not found.

    print('Banners by Clicks: ' + str(use_length))
    top_grossing += new_banners

    c = 0
    while len(top_grossing) < 5:
        top_grossing.append(random.randint(100, 500))
        c += 1
    print('Random Banners: ' + str(c))


if __name__ == '__main__':
    # app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
