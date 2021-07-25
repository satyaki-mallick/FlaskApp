
from pymongo import MongoClient
import redis
import pprint

mongo_client = MongoClient("mongodb+srv://db-admin-satyaki:admin@cluster0.kkrlk.mongodb.net/"
                           "MyFirstDatabase?retryWrites=true&w=majority")

# Localhost connection
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Redislab Connection
# redis_client = redis.Redis(host='redis-18192.c1.us-west-2-2.ec2.cloud.redislabs.com',
#                            password='iLSHqNBV7tRi47OF5kPB5CglDc47TktX',
#                            port=18192, decode_responses=True)

# AWS Lightsail Connection
# redis_client = redis.Redis(host='redis-service.9u64k1kqvn9po.us-west-2.cs.amazonlightsail.com',
#                          port=6379, decode_responses=True)
