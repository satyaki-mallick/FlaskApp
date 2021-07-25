

from prod.db_connection import mongo_client, redis_client
import unittest
import requests

BASE_URL = 'https://flask-service.9u64k1kqvn9po.us-west-2.cs.amazonlightsail.com/'
# BASE_URL = 'http://localhost:5000'


class FlaskTestCase(unittest.TestCase):

    URL = 'flask-service.9u64k1kqvn9po.us-west-2.cs.amazonlightsail.com:5000/campaign/44'

    def test_index(self):

        r = requests.get(BASE_URL)
        self.assertEqual(r.status_code, 200)

    def test_campaign_url(self):
        campaign_url = BASE_URL + "/campaign/44"
        r = requests.get(campaign_url)
        self.assertEqual(r.status_code, 200)

    def test_mongo(self):
        db = mongo_client['MyFirstDatabase']
        collection = db['clicks_1']
        item = collection.find_one()
        self.assertTrue(item)

    def test_redis(self):
        redis_client.set('foo', 'bar')
        self.assertEqual(redis_client.get('foo'), 'bar')


if __name__ == "__main__":
     unittest.main()