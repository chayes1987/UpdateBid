__author__ = 'Conor'

# The official documentation was consulted for all 3rd party libraries used
# 0mq -> https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/patterns/pubsub.html
# Firebase -> https://pypi.python.org/pypi/python-firebase/1.2
# Coding Standards -> https://www.python.org/dev/peps/pep-0008/

import zmq
import threading

context = zmq.Context()
publisher = None
my_firebase = None


class UpdateBid:
    """
    This class is responsible for updating the bid of an auction

    Attributes:
      context (0mq context): A 0mq context.
      publisher (0mq publisher): A 0mq publisher.
      my_firebase (Firebase): The firebase reference URL.
    """

    def __init__(self, firebase):
        """
        Constructor
        :param firebase: The firebase reference URL
        :return: Nothing
        """
        global my_firebase
        my_firebase = firebase

    @staticmethod
    def parse_message(message, start_tag, end_tag):
        """
        Parses received messages
        :param message: The message to parse
        :param start_tag: The starting delimiter
        :param end_tag: The ending delimiter
        :return: The required string
        """
        start_index = message.index(start_tag) + len(start_tag)
        substring = message[start_index:]
        end_index = substring.index(end_tag)
        return substring[:end_index]

    @staticmethod
    def initialize_publisher(ack_addr):
        """
        Initializes the 0mq publisher object
        :param ack_addr: The address to bind to for publishing acknowledgements
        :return: Nothing
        """
        global publisher
        publisher = context.socket(zmq.PUB)
        publisher.bind(ack_addr)

    @staticmethod
    def publish_acknowledgement(msg):
        """
        Publishes the acknowledgement to the UpdateBid command
        :param msg: The message to publish
        :return: Nothing
        """
        if None != publisher:
            # Publish the acknowledgement
            bid_changed_acknowledgement = 'ACK ' + msg
            publisher.send_string(bid_changed_acknowledgement)
            print('PUB: ' + bid_changed_acknowledgement)

    @staticmethod
    def update_bid(auction_id, bid):
        """
        Updates the current bid in Firebase
        :param auction_id: The ID of the auction
        :param bid: The value of the current bid
        :return: Nothing
        """
        try:
            # Update the Firebase values
            my_firebase.put('/auctions/' + auction_id, 'status', 'Running')
            my_firebase.put('/auctions/' + auction_id, 'current_bid', bid)
            print('Bid updated to ' + bid)
        except Exception:
            print('Could not perform update...')
            pass

    def initialize_heartbeat_subscriber(self, heartbeat_addr, hb_topic, response_topic, service_name):
        """
        Initializes the subscriber for the heartbeat functionality
        :param heartbeat_addr: The address to connect to
        :param hb_topic: The topic to subscribe to - CheckHeartbeat
        :param response_topic: The topic to respond with - Ok
        :param service_name: The name of the service to respond with - ScheduleAuction
        :return: Nothing
        """
        heartbeat_thread = threading.Thread(target=self.subscribe_to_heartbeat,
                                            kwargs={'heartbeat_addr': heartbeat_addr, 'heartbeat_topic': str(hb_topic),
                                                    'response_topic': response_topic, 'service_name': service_name},
                                            name='subscribe_to_heartbeat')
        heartbeat_thread.daemon = True
        heartbeat_thread.start()

    @staticmethod
    def subscribe_to_heartbeat(heartbeat_addr, heartbeat_topic, response_topic, service_name):
        """
        Subscribe to the Heartbeat functionality
        :param heartbeat_addr: The address to connect to
        :param heartbeat_topic: The topic to subscribe to - CheckHeartbeat
        :param response_topic: The topic to respond with - Ok
        :param service_name: The name of the service to respond with - ScheduleAuction
        :return: Nothing
        """
        heartbeat_subscriber = context.socket(zmq.SUB)
        # Connect to the address and set the topic to subscribe to
        heartbeat_subscriber.connect(heartbeat_addr)
        heartbeat_subscriber.setsockopt(zmq.SUBSCRIBE, str.encode(heartbeat_topic))

        while True:
            print('REC: ' + heartbeat_subscriber.recv().decode())
            # Build and send the response immediately
            heartbeat_response = response_topic + ' <params>' + service_name + '</params>'
            publisher.send_string(heartbeat_response)
            print('PUB: ' + heartbeat_response)

    def subscribe_to_update_bid(self, sub_addr, topic):
        """
        Subscribe to the UpdateBid command
        :param sub_addr: The address to connect to
        :param topic: The topic to subscribe to
        :return: Nothing
        """
        update_bid_subscriber = context.socket(zmq.SUB)
        # Connect to the address and set the topic to subscribe to
        update_bid_subscriber.connect(sub_addr)
        update_bid_subscriber.setsockopt(zmq.SUBSCRIBE, str.encode(str(topic)))
        print('SUB: ' + topic)

        while True:
            try:
                update_bid = update_bid_subscriber.recv()
                update_bid_str = update_bid.decode()
                print('REC: ' + update_bid_str)
                # Publish the acknowledgement
                self.publish_acknowledgement(update_bid_str)
                # Extract the ID and the current bid
                auction_id = self.parse_message(update_bid_str, '<id>', '</id>')
                bid = self.parse_message(update_bid_str, '<params>', '</params>')
                # Update Firebase
                self.update_bid(auction_id, bid)
            except (KeyboardInterrupt, SystemExit):
                print('Application Stopped...')
                raise SystemExit