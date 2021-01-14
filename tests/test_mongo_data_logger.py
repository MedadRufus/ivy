from unittest import TestCase
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from util import mongo_data_logger

class TestMongoLogger(TestCase):
    def setUp(self) -> None:
        self.ml = mongo_data_logger.MongoLogger()

    def test_get_server_uuid(self):
        print(self.ml.get_server_uuid())
