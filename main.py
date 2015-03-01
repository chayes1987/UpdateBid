__author__ = 'Conor'

# Firebase -> https://pypi.python.org/pypi/python-firebase/1.2
# Config file -> https://docs.python.org/2/library/configparser.html

from updatebid import UpdateBid
from configparser import ConfigParser, Error
from firebase import firebase
from config import Config


def read_config():
    conf = ConfigParser()
    try:
        conf.read_file(open('config.ini'))
        pub_addr = conf.get('Addresses', 'PUB_ADDR')
        sub_addr = conf.get('Addresses', 'SUB_ADDR')
        topic = conf.get('Topics', 'BID_CHANGED_TOPIC')
        firebase_url = conf.get('Firebase', 'FIREBASE_URL')
    except (IOError, Error):
        print('Error with config file...')
        return None

    return pub_addr, sub_addr, topic, firebase_url


if __name__ == '__main__':
    configuration = read_config()
    if None != configuration:
        my_firebase = firebase.FirebaseApplication(configuration[Config.FIREBASE_URL], authentication=None)
        updater = UpdateBid(my_firebase)
        updater.initialize_publisher(configuration[Config.PUB_ADDRESS])
        print('Publisher initialized...')
        updater.initialize_subscriber(configuration[Config.SUB_ADDRESS], configuration[Config.TOPIC])