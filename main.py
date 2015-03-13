__author__ = 'Conor'

# Firebase -> https://pypi.python.org/pypi/python-firebase/1.2
# Config file -> https://docs.python.org/2/library/configparser.html

from updatebid import UpdateBid
from configparser import ConfigParser, Error
from firebase import firebase
from config import Config


def read_config():
    configuration = ConfigParser()
    try:
        configuration.read_file(open('config.ini'))
        pub_addr = configuration.get('Addresses', 'PUB_ADDR')
        sub_addr = configuration.get('Addresses', 'SUB_ADDR')
        heartbeat_addr = configuration.get('Addresses', 'HEARTBEAT_ADDR')
        topic = configuration.get('Topics', 'BID_CHANGED_TOPIC')
        firebase_url = configuration.get('Firebase', 'FIREBASE_URL')
        heartbeat_topic = configuration.get('Topics', 'CHECK_HEARTBEAT_TOPIC')
        response_topic = configuration.get('Topics', 'CHECK_HEARTBEAT_TOPIC_RESPONSE')
        service_name = configuration.get('Service Name', 'SERVICE_NAME')
    except (IOError, Error):
        print('Error with config file...')
        return None

    return pub_addr, sub_addr, topic, firebase_url, heartbeat_addr, heartbeat_topic, response_topic, service_name


if __name__ == '__main__':
    config = read_config()
    if None != config:
        my_firebase = firebase.FirebaseApplication(config[Config.FIREBASE_URL], authentication=None)
        updater = UpdateBid(my_firebase)
        updater.initialize_publisher(config[Config.PUB_ADDRESS])
        print('Publisher initialized...')
        updater.initialize_subscribers(config[Config.SUB_ADDRESS], config[Config.TOPIC], config[Config.HEARTBEAT_ADDR],
                                       config[Config.HEARTBEAT_TOPIC], config[Config.RESPONSE_TOPIC],
                                       config[Config.SERVICE_NAME])