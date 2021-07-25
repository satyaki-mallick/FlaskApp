
from dev import populate_db_script
import unittest

database = 'TestDb3'


class FlaskTestCase(unittest.TestCase):

    def test_normal_insert(self):
        message = populate_db_script.mongoimport('./test_csv/test_conversions_01.csv', database, 'test_conversions_1')
        self.assertEqual("All items in csv inserted", message)

    def test_same_csv_insert_again(self):
        message = populate_db_script.mongoimport('./test_csv/test_conversions_01.csv', database, 'test_conversions_1')
        self.assertEqual("csv is already uploaded", message)
    """"""
    def test_different_column_names(self):
        message = populate_db_script.mongoimport('./test_csv/test_conversions_02.csv', database, 'test_conversions_1')
        self.assertEqual("Column names do not match", message)

    def test_extra_items_in_csv(self):
        message = populate_db_script.mongoimport('./test_csv/test_conversions_03.csv', database, 'test_conversions_1')
        self.assertIn("Part of the csv is new.", message)

    def test_extra_items_in_DB(self):
        message = populate_db_script.mongoimport('./test_csv/test_conversions_04.csv', database, 'test_conversions_1')
        self.assertIn("DB contains extra items than is given by the csv.", message)


