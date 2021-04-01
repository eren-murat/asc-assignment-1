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
    
        self.products = {}

        self.carts = {}
        self.num_producers = 0
        self.num_carts = 0
        self.lock_new_cart = Lock()
        self.lock_producers = Lock()
        self.lock_manage_cart = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.lock_producers:
            new_producer_id = self.num_producers
            self.num_producers += 1
        self.products[str(new_producer_id)] = []
        return str(new_producer_id)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if len(self.products[producer_id]) >= self.queue_size_per_producer:
            return False

        self.products[producer_id].append(product)

        print(self.products)

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        for each new cart, a new empty list is inserted into the carts list
        """
        # with self.lock_new_cart:
        new_cart_id = self.num_carts
        self.num_carts += 1
        self.carts[str(new_cart_id)] = []
        return str(new_cart_id)

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # print(self.carts[cart_id])
        # print(product)
        # print("###")

        # with self.lock_manage_cart:
        found = False
        for key, value in self.products.items():
            if product in value:
                found = True
                index = key
                break
        if found:
            self.carts[cart_id].append((product, index))
            self.products[index].remove(product)
            return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        with self.lock_manage_cart:
            index = -1
            for key, value in self.carts.items():
                for (prod, producer_id) in value:
                    if prod == value:
                        index = int(producer_id)
                        break
            if index > -1:
                self.carts[cart_id].remove((product, index))
                self.products[str(index)].append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        order = self.carts[str(cart_id)]

        # for product, producer_id in order:
        #     print("{0} bought {1}".format(currentThread().getName(), product))
        # return order
        
