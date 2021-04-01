# ASC-assigment1
Producer-Consumer implementation in python 3.8 for ASC class.

Eren Murat, 334CA

Structure:
    My solution is build around two dictionaries in marketplace. The first one is
products. It is mapped after the producer ids and contains the lists of products
for each producer. The second dictionary is carts. It is mapped after the cart ids
and contains list of tuples. Each tuple is formed by the product and the producer id.
This is necessary in order to remember where to place the product if a consumer
decides to remove it from his cart.
    I found the assignment useful because it was a great opportunity to work
on my python skills.
    I believe that my implementation is fairly efficient, especially storage wise.
I do not think that I store unnecessary information thanks to those two dictionaries.

Implementation:
    I implemented all the points specified.
    A small interesting thing is that when I print the order, I can not simply get
the list by id from carts. I have to unpack it into a new list because I also stored
the producer id.
    Another interesting thing that I learned is how to ignore the index in a loop:
                for _ in range(10):     
                    do_something()
    This was useful for coding style!

Repository:
    I added the .git folder, I could add the link, but the repo is private anyway.