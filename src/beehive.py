import random
from flowers import load_flowers

# initialize RUCHE position

BEEHIVE = (500, 500)


# initialize Bee class with path= None
class Bee:

    def __init__(self, flowers, path=None):
        self.flowers = flowers

        if path is None:
            # copy of flowers to initialize random path
            self.path = list(flowers)
            random.shuffle(self.path)
        else:
            self.path = path

        self.distance = 0


# initialize Beehive


class Beehive:

    def __init__(self, flowers, size=101):
        self.flowers = flowers
        self.bees = []  # save 101 bees

        for i in range(size):
            new_bee = Bee(flowers)
            # each loop saving new bees, flowers path
            self.bees.append(new_bee)

        self.queen = None
