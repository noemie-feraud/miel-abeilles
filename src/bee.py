import random
import math

from config import BEEHIVE


# initialize Bee class with path= None


class Bee:

    def __init__(self, flower, path=None):
        self.flower = flower

        if path is None:
            # copy of flower to initialize random path
            self.path = list(flower)
            random.shuffle(self.path)
        else:
            self.path = path
    
        self.distance = 0

    def compute_segment(self, p1, p2):
        length = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
        return length ** 0.5

    def compute_path_length(self, path=None):
        """
        Ruche A - B - ..-Z - Beehive
            (path)
        We want the perimeter of a polygon with n +1 sides,
        n being the number of flowers
        """
        if path is None:
            path = self.path

        length = 0
        length += self.compute_segment(BEEHIVE, path[0])

        for i in range(len(path) - 1):
            length += self.compute_segment(path[i], path[i + 1])

        length += self.compute_segment(path[-1], BEEHIVE)

        self.distance = length
        return length

    def mutate (self):
        
        """Échange deux fleurs au hasard dans le chemin de l'abeille."""
        
        fist_f = random.randint(0, len(self.path) - 1)
        last_f = random.randint(0, len(self.path) - 1)
        
        # On inverse les deux fleurs
        self.path[fist_f], self.path[last_f] = self.path[last_f], self.path[fist_f]
        
        # On recalcule sa nouvelle distance
        self.compute_path_length()





    def __str__(self):
        return f"Bee(distance={self.distance:.2f})"






        


