"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock, currentThread

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.lock_producers = Lock()
        self.lock_add_to_cart = Lock()
        self.lock_new_cart = Lock()
        self.lock_order = Lock()
        self.products = {}
        self.carts = {}
        self.count_carts = 0
        self.count_producers = 0

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # Each producers is assigned the order number as id
        with self.lock_producers:
            producer_id = str(self.count_producers)
            self.count_producers += 1
        self.products[producer_id] = []
        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # Verify if the number of products in his list exceeds the max
        # If there is still room, add the product in the correct list by id
        if len(self.products[producer_id]) >= self.queue_size_per_producer:
            return False
        self.products[producer_id].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        for each new cart, a new empty list is inserted into the carts list
        """
        # Each cart is assigned the order number as id
        with self.lock_new_cart:
            cart_id = str(self.count_carts)
            self.count_carts += 1
        self.carts[cart_id] = []
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # Search in every producer list for the desired product
        # If it is found, it is added in the cart with the producer_id to remember where to
        # put it back
        with self.lock_add_to_cart:
            found = False
            for key, value in self.products.items():
                if product in value:
                    producer_id = key
                    found = True
            if found is False:
                return False
        self.carts[cart_id].append((product, producer_id))
        self.products[producer_id].remove(product)
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # Find the producer_id of the product, so it can be added back in the correct list
        for (prod, producer_id) in self.carts[cart_id]:
            if prod == product:
                p_id = producer_id
        self.carts[cart_id].remove((product, p_id))
        self.products[p_id].append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # Products are stored in carts with the producer_id, so they are unpacked in a new list
        order = []
        for product, _ in self.carts[cart_id]:
            order.append(product)
        for product in order:
            with self.lock_order:
                print("{0} bought {1}".format(currentThread().getName(), product))
        return order
