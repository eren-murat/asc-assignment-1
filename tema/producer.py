"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):
        # Loop continuosly through the list of products and try to publish them
        # When the publish function returns false, the producer waits the republis_wait_time
        # and then tries to publish the same product again, thus making sure that the
        # desired quantity of each product is published
        # When the publish function returns true, the producer waits the normal_wait_time
        # and the quantity to be published is decreased
        new_producer_id = self.marketplace.register_producer()
        while True:
            for (prod, quantity, normal_wait_time) in self.products:
                quant = quantity
                while quant > 0:
                    if self.marketplace.publish(new_producer_id, prod):
                        time.sleep(normal_wait_time)
                        quant -= 1
                    else:
                        time.sleep(self.republish_wait_time)
