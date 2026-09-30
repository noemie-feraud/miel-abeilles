"""Parameter study: one parameter at a time, averaged over several seeds."""

import numpy as np

from beehive import Beehive, load_field
from config import FLOWERS_PATH, NB_GENERATIONS

SEEDS = range(5)


def final_best(flowers, seed, **parameters):
    """Run one full simulation, return the best distance at the end."""
    hive = Beehive(flowers, seed=seed, **parameters)
    hive.init_bees()
    for _ in range(NB_GENERATIONS):
        hive.next_generation()
    return hive.bees[0].distance


def sweep(flowers, name, values):
    """Vary one parameter, average the result over the seeds."""
    print(f"\n--- {name} ---")
    for value in values:
        results = [final_best(flowers, seed, **{name: value}) for seed in SEEDS]
        print(f"{name}={str(value):>5}   mean {np.mean(results):8.0f}"
              f"   std {np.std(results):6.0f}")


def sweep_pairs(flowers, pairs, seeds=range(12)):
    """Test parameter combinations, since one-at-a-time sweeps miss interactions."""
    print("\n--- combinations ---")
    for tournament_size, mutation_rate in pairs:
        results = [final_best(flowers, seed,
                              tournament_size=tournament_size,
                              mutation_rate=mutation_rate)
                   for seed in seeds]
        print(f"tournament={tournament_size:>3}  mutation={mutation_rate:>4}"
              f"   mean {np.mean(results):8.0f}   std {np.std(results):6.0f}")


def main():
    flowers = load_field(FLOWERS_PATH)
    sweep(flowers, "tournament_size", [2, 3, 5, 10, 20])
    sweep(flowers, "mutation_rate", [0.0, 0.1, 0.3, 0.5, 0.8, 1.0])
    sweep(flowers, "nb_elites", [0, 1, 5, 10, 25, 50])
    sweep_pairs(flowers, [(3, 0.3), (10, 0.5), (20, 0.7), (50, 0.9), (100, 0.9)])


if __name__ == "__main__":
    main()