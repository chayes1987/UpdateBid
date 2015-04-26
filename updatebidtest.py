__author__ = 'Conor'

# Unit Testing -> https://docs.python.org/3/library/unittest.html
# Coding Standards -> https://www.python.org/dev/peps/pep-0008/

import unittest
from updatebid import UpdateBid
from main import read_config
from config import Config


class UpdateBidTests(unittest.TestCase):
    """
    This class is responsible for testing some functions in UpdateBid

    """

    def test_parse_message(self):
        """
        Tests the parse_message function
        :return: Assertion results
        """
        update_bid = UpdateBid(None)
        self.assertEqual("hello world", update_bid.parse_message('#hello world&', '#', '&'))
        self.assertEqual("hello", update_bid.parse_message('#hello&world&', '#', '&'))
        self.assertNotEqual("hello world", update_bid.parse_message('#hello world&', '#', 'o'))
        self.assertEqual("1", update_bid.parse_message('<id>1</id>', '<id>', '</id>'))
        self.assertEqual("2000", update_bid.parse_message('<params>2000</params>', '<params>', '</params>'))

    def test_read_config(self):
        """
        Tests the read_config function
        :return: Assertion results
        """
        config = read_config()
        self.assertNotEqual(None, config)
        self.assertEqual('tcp://*:2500', config[Config.PUB_ADDR])
        self.assertEqual('tcp://172.31.32.23:2360', config[Config.SUB_ADDR])
        self.assertEqual('BidChanged', config[Config.TOPIC])
        self.assertEqual('https://auctionapp.firebaseio.com', config[Config.FIREBASE_URL])

if __name__ == '__main__':
    unittest.main()
