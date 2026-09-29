import random

from bee import Bee
from config import NB_BEES


class Beehive:

    def __init__(self, flower, size=NB_BEES):
        self.flower = flower
        self.size = size
        self.bees = []
        self.queen = None

    def init_bees(self):
        """Initialise la population de 'size' abeilles avec des chemins aléatoires."""
        self.bees = []
        for _ in range(self.size):
            new_bee = Bee(self.flower)
            new_bee.calculate_distance()
            self.bees.append(new_bee)

    

    def print_average_distance(self):
        """Calcule et affiche la distance moyenne parcourue par les abeilles de la ruche."""
        if not self.bees:
            print("Aucune abeille dans la ruche.")
            return 0

        total_distance = sum(bee.distance for bee in self.bees)
        average = total_distance / len(self.bees)
        print(f"Distance moyenne : {average:.2f}")
        return average

    def next_generation(self):
        """ la génération suivante d'abeilles.
        methoide pour trier les abeilles selon leur distance 
        distance la plus courte en premier  """

        def key_distance(bee):
            return bee.distance
        
        self.bees.sort(key=key_distance)
        self.queen = self.bees[0]

        """ On garde les 20 abeilles les plus performantes et on en initialise 81 autres pour ruche= 101
        parent en random """
        
        perform = self.bees[:20]

        for _ in range(81):

            parent1 = random.choice(perform)
            parent2 = random.choice(perform)

            chemin_enfant = list(parent1.path[:25])  # la moitié des 50 fleurs

            for flower in parent2.path:
                if flower not in chemin_enfant:
                    chemin_enfant.append(flower)

        


        

    def __str__(self):
        return f"Beehive(abeilles={len(self.bees)}, fleurs={len(self.flower)})"
