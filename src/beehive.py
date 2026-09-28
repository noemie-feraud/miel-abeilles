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
            new_bee.compute_path_length()
            self.bees.append(new_bee)

    # Alias au cas où la méthode est appelée au singulier
    init_bee = init_bees

    def print_average_distance(self):
        """Calcule et affiche la distance moyenne parcourue par les abeilles de la ruche."""
        if not self.bees:
            print("Aucune abeille dans la ruche.")
            return 0

        total_distance = sum(bee.distance for bee in self.bees)
        average = total_distance / len(self.bees)
        print(f"Distance moyenne : {average:.2f}")
        return average

    # Alias au cas où l'ancien nom de beehive2 est utilisé
    print_average_path_length = print_average_distance

    def next_generation(self):
        """Prépare la génération suivante d'abeilles (pour la suite du projet)."""
        pass

    def __str__(self):
        return f"Beehive(abeilles={len(self.bees)}, fleurs={len(self.flower)})"
