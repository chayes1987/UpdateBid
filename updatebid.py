__author__ = 'Conor'

# The official documentation was consulted for all three 3rd party libraries used
# ZeroMQ -> https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/patterns/pubsub.html
# Firebase -> https://pypi.python.org/pypi/python-firebase/1.2

import zmq
import threading

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
            bid_changed_acknowledgement = 'ACK ' + msg
            publisher.send_string(bid_changed_acknowledgement)
            print('PUB: ' + bid_changed_acknowledgement)

    @staticmethod
    def update_bid(auction_id, bid):
        try:
            my_firebase.put('/auctions/' + auction_id, 'status', 'Running')
            my_firebase.put('/auctions/' + auction_id, 'current_bid', bid)
            print('Bid updated to ' + bid)
        except Exception:
            print('Could not perform update...')
            pass

    def initialize_heartbeat_subscriber(self, heartbeat_addr, hb_topic, response_topic, service_name):
        heartbeat_thread = threading.Thread(target=self.subscribe_to_heartbeat,
                                            kwargs={'heartbeat_addr': heartbeat_addr, 'heartbeat_topic': str(hb_topic),
                                                    'response_topic': response_topic, 'service_name': service_name},
                                            name='subscribe_to_heartbeat')
        heartbeat_thread.daemon = True
        heartbeat_thread.start()

    @staticmethod
    def subscribe_to_heartbeat(heartbeat_addr, heartbeat_topic, response_topic, service_name):
        heartbeat_subscriber = context.socket(zmq.SUB)
        heartbeat_subscriber.connect(heartbeat_addr)
        heartbeat_subscriber.setsockopt(zmq.SUBSCRIBE, str.encode(heartbeat_topic))

        while True:
            print('REC: ' + heartbeat_subscriber.recv().decode())
            heartbeat_response = response_topic + ' <params>' + service_name + '</params>'
            publisher.send_string(heartbeat_response)
            print('PUB: ' + heartbeat_response)

    def subscribe_to_update_bid(self, sub_addr, topic):
        update_bid_subscriber = context.socket(zmq.SUB)
        update_bid_subscriber.connect(sub_addr)
        update_bid_subscriber.setsockopt(zmq.SUBSCRIBE, str.encode(str(topic)))
        print('SUB: ' + topic)

        while True:
            try:
                update_bid = update_bid_subscriber.recv()
                update_bid_str = update_bid.decode()
                print('REC: ' + update_bid_str)
                self.publish_acknowledgement(update_bid_str)
                auction_id = self.parse_message(update_bid_str, '<id>', '</id>')
                bid = self.parse_message(update_bid_str, '<params>', '</params>')
                self.update_bid(auction_id, bid)
            except (KeyboardInterrupt, SystemExit):
                print('Application Stopped...')
                raise SystemExit