import csv

from beehive import Beehive
from config import DATA_PATH, BEEHIVE, NB_GENERATIONS


def load_data(path):
    flower = []

    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)  # skipping the header

        for row in reader:
            flower.append((int(row[0]), int(row[1])))

    return flower


def main():

    flower = load_data(DATA_PATH)
    print(f"Nombre de fleurs chargées : {len(flower)}")
    print(f"Premières fleurs : {flower[:3]}")
    b = Beehive(flower)
    b.init_bee()
    
    for i in range (NB_GENERATIONS):
        b.next_generation()
        b.print_average_distance()
    


# Point d'entrée du programme
if __name__ == "__main__":
    main()
