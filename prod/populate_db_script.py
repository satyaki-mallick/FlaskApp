

from pymongo import MongoClient
import pandas as pd
import json

mongo_client = MongoClient("mongodb+srv://db-admin-satyaki:admin@cluster0.kkrlk.mongodb.net/"
                           "MyFirstDatabase?retryWrites=true&w=majority")
database = 'TestDb2'


def mongoimport(csv_path, db_name, coll_name):

    db = mongo_client[db_name]
    log_collection = db['logging']
    existing_collection = db[coll_name]
    existing_df = existing_collection.find_one()

    new_df = pd.read_csv(csv_path)

    if not existing_df:
        coll = db[coll_name]
        payload = json.loads(new_df.to_json(orient='records'))
        coll.remove()
        coll.insert_many(payload)

    else:
        existing_df = pd.DataFrame(list(db[coll_name].find()))
        del existing_df['_id']

        if new_df.index.names != existing_df.index.names:
            print("Column names do not match")

            log = {"file_path": csv_path,
                   "error": "Column names do not match",
                   "action": "Rejected"
                   }
            log_collection.insert_one(log)

        elif new_df.equals(existing_df):
            print("csv is already uploaded")

            log = {"file_path": csv_path,
                   "error": "exact collection already exists",
                   "action": "Rejected"
                   }
            log_collection.insert_one(log)

        else:
            merged_df = existing_df.merge(new_df, indicator=True, how='outer')
            changed_rows_df = merged_df[merged_df['_merge'] == 'right_only']
            new_rows = changed_rows_df.drop('_merge', axis=1)

            payload = json.loads(new_rows.to_json(orient='records'))
            if not payload:

                print("DB contains extra items than is given by the csv. DB data was not changed")
                """Log"""
                log = {"file_path": csv_path,
                       "error": "DB contains extra items than is given by the csv",
                       "action": "DB data was not changed"
                       }
                log_collection.insert_one(log)

            else:
                existing_collection.insert_many(payload)

                message = "Part of the csv is new. {} new items are appended to collection".format(len(new_rows))

                print(message)
                """Log"""
                log = {"file_path": csv_path,
                       "error": "Part of the csv is new",
                       "action": message
                       }
                log_collection.insert_one(log)


if __name__ == "__main__":
    mongoimport('../csv/1/conversions_1.csv', database, 'conversions_1')
    # mongoimport('../csv/2/conversions_2.csv', database, 'conversions_2')
    # mongoimport('../csv/3/conversions_3.csv', database, 'conversions_3')
    # mongoimport('../csv/4/conversions_4.csv', database, 'conversions_4')
    #
    #
    # mongoimport('../csv/1/clicks_1.csv', database, 'clicks_1')
    # mongoimport('../csv/2/clicks_2.csv', database, 'clicks_2')
    # mongoimport('../csv/3/clicks_3.csv', database, 'clicks_3')
    # mongoimport('../csv/4/clicks_4.csv', database, 'clicks_4')
