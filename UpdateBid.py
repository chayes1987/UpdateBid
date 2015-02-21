__author__ = 'Conor'

# The official documentation was consulted for all three 3rd party libraries used
# ZeroMQ -> https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/patterns/pubsub.html
# Firebase -> https://pypi.python.org/pypi/python-firebase/1.2

from firebase import firebase
import zmq

publisher = None
context = zmq.Context()
SUBSCRIBER_ADDRESS = 'tcp://172.31.32.23:2360'
ACK_ADDRESS = 'tcp://*:2500'
FIREBASE_URL = 'https://auctionapp.firebaseio.com'
my_firebase = firebase.FirebaseApplication(FIREBASE_URL, authentication=None)


class UpdateBid:

    @staticmethod
    def parse_message(message, start_tag, end_tag):
        start_index = message.index(start_tag) + len(start_tag)
        substring = message[start_index:]
        end_index = substring.index(end_tag)
        return substring[:end_index]

    @staticmethod
    def publish_acknowledgement(msg):
        if None != publisher:
            message = 'ACK: ' + msg
            publisher.send_string(message)
            print('ACK SENT...')

    @staticmethod
    def update_bid(auction_id, bid):
        try:
            my_firebase.put('/auctions/' + auction_id, 'status', 'Running')
            my_firebase.put('/auctions/' + auction_id, 'current_bid', bid)
            print('Bid updated to ' + bid)
        except Exception:
            print('Could not perform update...')
            pass

    def initialize_subscriber(self):
        subscriber = context.socket(zmq.SUB)
        subscriber.connect(SUBSCRIBER_ADDRESS)
        subscriber.setsockopt(zmq.SUBSCRIBE, str.encode('BidChanged'))
        print('SUB: BidChanged')

        while True:
            msg = subscriber.recv()
            m = msg.decode()
            print('REC: ' + m)
            self.publish_acknowledgement(m)
            auction_id = self.parse_message(m, '<id>', '</id>')
            bid = self.parse_message(m, '<params>', '</params>')
            self.update_bid(auction_id, bid)

    @staticmethod
    def initialize_publisher():
        global publisher
        publisher = context.socket(zmq.PUB)
        publisher.bind(ACK_ADDRESS)

if __name__ == '__main__':
    updater = UpdateBid()
    updater.initialize_publisher()
    print('Publisher initialized...')
    updater.initialize_subscriber()