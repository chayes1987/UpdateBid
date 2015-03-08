from main import read_config

__author__ = 'Conor'

import unittest
from updatebid import UpdateBid
from config import Config


class UpdateBidTests(unittest.TestCase):

    def test_parse_message(self):
        update_bid = UpdateBid(None)
        self.assertEqual("hello world", update_bid.parse_message('#hello world&', '#', '&'))
        self.assertEqual("hello", update_bid.parse_message('#hello&world&', '#', '&'))
        self.assertNotEqual("hello world", update_bid.parse_message('#hello world&', '#', 'o'))
        self.assertEqual("1", update_bid.parse_message('<id>1</id>', '<id>', '</id>'))
        self.assertEqual("2000", update_bid.parse_message('<params>2000</params>', '<params>', '</params>'))

    def test_read_config(self):
        config = read_config()
        self.assertNotEqual(None, config)
        self.assertEqual('tcp://*:2500', config[Config.PUB_ADDRESS])
        self.assertEqual('tcp://172.31.32.23:2360', config[Config.SUB_ADDRESS])
        self.assertEqual('BidChanged', config[Config.TOPIC])
        self.assertEqual('https://auctionapp.firebaseio.com', config[Config.FIREBASE_URL])

if __name__ == '__main__':
    unittest.main()
