__author__ = 'Conor'

# The official documentation was consulted for all three 3rd party libraries used
# ZeroMQ -> https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/patterns/pubsub.html
# Firebase -> https://pypi.python.org/pypi/python-firebase/1.2

import zmq

context = zmq.Context()
publisher = None
my_firebase = None


class UpdateBid:

    def __init__(self, firebase):
        global my_firebase
        my_firebase = firebase

    @staticmethod
    def parse_message(message, start_tag, end_tag):
        start_index = message.index(start_tag) + len(start_tag)
        substring = message[start_index:]
        end_index = substring.index(end_tag)
        return substring[:end_index]

    @staticmethod
    def initialize_publisher(ack_addr):
        global publisher
        publisher = context.socket(zmq.PUB)
        publisher.bind(ack_addr)

    @staticmethod
    def publish_acknowledgement(msg):
        if None != publisher:
            message = 'ACK ' + msg
            publisher.send_string(message)
            print('PUB: ' + message)

    @staticmethod
    def update_bid(auction_id, bid):
        try:
            my_firebase.put('/auctions/' + auction_id, 'status', 'Running')
            my_firebase.put('/auctions/' + auction_id, 'current_bid', bid)
            print('Bid updated to ' + bid)
        except Exception:
            print('Could not perform update...')
            pass

    def initialize_subscriber(self, sub_addr, topic):
        subscriber = context.socket(zmq.SUB)
        subscriber.connect(sub_addr)
        subscriber.setsockopt(zmq.SUBSCRIBE, str.encode(str(topic)))
        print('SUB: ' + topic)

        while True:
            try:
                msg = subscriber.recv()
                m = msg.decode()
                print('REC: ' + m)
                self.publish_acknowledgement(m)
                auction_id = self.parse_message(m, '<id>', '</id>')
                bid = self.parse_message(m, '<params>', '</params>')
                self.update_bid(auction_id, bid)
            except (KeyboardInterrupt, SystemExit):
                print('Application Stopped...')
                raise SystemExit