"""Entry point: build the hive, run the generations, report."""

from beehive import Beehive, load_field
from config import FLOWERS_PATH, NB_GENERATIONS
from plots import plot_convergence, plot_field, plot_tour

def main():
    hive = Beehive(load_field(FLOWERS_PATH), seed=0)
    hive.init_bees()
    print(hive)
    print(
        f"generation   0: "
        f"average {hive.average_distance():.0f}, "
        f"best {hive.bees[0].distance:.0f}"
    )

    for generation in range(1, NB_GENERATIONS + 1):
        hive.next_generation()
        if generation % 10 == 0:
            print(
                f"generation {generation:3d}: "
                f"average {hive.average_distance():.0f}, "
                f"best {hive.bees[0].distance:.0f}"
            )

    print("best bee:", hive.bees[0])
    best = hive.bees[0]
    plot_field(hive.flowers)
    plot_convergence(hive.history)
    plot_tour(hive.flowers, best.order, best.distance)


if __name__ == "__main__":
    main()