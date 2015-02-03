__author__ = 'Conor'

import zmq

publisher = None
context = zmq.Context()
SUBSCRIBER_ADDRESS = 'tcp://127.0.0.1:1111'
PUBLISHER_ADDRESS = 'tcp://127.0.0.1:2001'


class UpdateBid:

    @staticmethod
    def parse_message(message, start_tag, end_tag):
        start_index = message.index(start_tag) + len(start_tag)
        substring = message[start_index:]
        end_index = substring.index(end_tag)
        return substring[:end_index]

    def initialize_subscriber(self):
        subscriber = context.socket(zmq.SUB)
        subscriber.connect(SUBSCRIBER_ADDRESS)
        subscriber.setsockopt(zmq.SUBSCRIBE, str.encode('BidChanged'))
        print('Subscribed to BidChanged event...')

        while True:
            msg = subscriber.recv()
            m = msg.decode(encoding='UTF-8')
            print(m + ' received...')
            self.publish_acknowledgement(m)

    @staticmethod
    def initialize_publisher():
        global publisher
        publisher = context.socket(zmq.PUB)
        publisher.bind(PUBLISHER_ADDRESS)

if __name__ == '__main__':
    updater = UpdateBid()
    updater.initialize_publisher()
    print('Publisher initialized...')
    updater.initialize_subscriber()