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

    # Alias pour compatibilité
    calculate_distance = compute_path_length

    def __str__(self):
        return f"Bee(distance={self.distance:.2f})"






        


# DANS LA CLASSE Bee :

#     METHODE calculate_distance():
#         1. On part du point fixe de la ruche : (500, 500)
#         2. On initialise la distance_totale à 0

#         3. POUR CHAQUE fleur DANS self.path:
#             - Calculer la distance entre la position actuelle et cette fleur
#               Formule : √((x2 - x1)² + (y2 - y1)²)
#             - Ajouter cette distance à distance_totale
#             - La fleur devient la nouvelle position actuelle

#         4. Ajouter la distance du retour : dernière fleur -> ruche (500, 500)

#         5. Stocker le résultat dans self.distance et le retourner
