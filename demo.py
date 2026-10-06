"""Live demos for the oral: one short command per demo.

    uv run python demo.py brute       slide 6  - exhaustive search vs genetic algorithm
    uv run python demo.py speed       slide 8  - distance matrix vs recomputing distances
    uv run python demo.py crossover   slide 10 - naive crossover vs the one we use
    uv run python demo.py mutation    slide 10 - swap breaks 4 links, reverse breaks 2
"""

import itertools
import math
import sys
import time

import numpy as np

from beehive import (BEEHIVE_POSITION, Beehive, build_distance_matrix, crossover,
                     generate_field, load_field, path_length)
from config import FLOWERS_PATH


def demo_brute():
    """Slide 6: every order on 9 flowers, then why 50 flowers is out of reach."""
    flowers = generate_field(9, seed=42)
    distances = build_distance_matrix(flowers)
    start = time.perf_counter()
    orders = np.array(list(itertools.permutations(range(9))), dtype=np.int64) + 1
    best = np.inf
    for chunk in np.array_split(orders, 40):
        hive = np.zeros((len(chunk), 1), dtype=np.int64)
        steps = np.hstack([hive, chunk, hive])
        best = min(best, distances[steps[:, :-1], steps[:, 1:]].sum(axis=1).min())
    elapsed = time.perf_counter() - start
    print(f"9 flowers : {len(orders):,} possible tours, all tested in {elapsed:.2f} s")
    print(f"  exact optimum      : {best:.0f}")

    hive = Beehive(flowers, seed=0)
    hive.init_bees()
    for _ in range(100):
        hive.next_generation()
    print(f"  genetic algorithm  : {hive.bees[0].distance:.0f}")
    print()
    print(f"50 flowers : 50! = {math.factorial(50):.2e} possible tours")
    print(f"  at the same speed  : about {math.factorial(50) / len(orders) * elapsed / 3.15e7:.1e} years")


def demo_speed():
    """Slide 8: read distances from the matrix instead of recomputing them."""
    flowers = load_field(FLOWERS_PATH)
    distances = build_distance_matrix(flowers)
    rng = np.random.default_rng(0)
    orders = [rng.permutation(50) for _ in range(9000)]

    coords = [[tuple(flowers[i]) for i in o] for o in orders]

    def segment(p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def by_coordinates(path):
        length = segment(BEEHIVE_POSITION, path[0])
        for i in range(len(path) - 1):
            length += segment(path[i], path[i + 1])
        return length + segment(path[-1], BEEHIVE_POSITION)

    start = time.perf_counter()
    slow = [by_coordinates(p) for p in coords]
    t_slow = time.perf_counter() - start
    start = time.perf_counter()
    fast = [path_length(o, distances) for o in orders]
    t_fast = time.perf_counter() - start

    print(f"distance matrix : {distances.shape[0]} x {distances.shape[1]}, computed once")
    print(f"9,000 bees evaluated, same results : {np.allclose(slow, fast)}")
    print(f"  recomputing every distance : {t_slow:.3f} s")
    print(f"  reading the matrix         : {t_fast:.3f} s")
    print(f"  {t_slow / t_fast:.1f} times faster")


def demo_crossover():
    """Slide 10: the naive crossover silently breaks the tour."""
    rng = np.random.default_rng(0)
    mother = rng.permutation(50)
    father = rng.permutation(50)

    naive = np.concatenate([mother[:25], father[25:]])
    values, counts = np.unique(naive, return_counts=True)
    print("NAIVE: head of the mother + tail of the father")
    print(f"  length            : {len(naive)}")
    print(f"  distinct flowers  : {len(values)} / 50")
    print(f"  visited twice     : {values[counts == 2].tolist()}")
    print(f"  never visited     : {sorted(set(range(50)) - set(naive.tolist()))}")
    print()
    child = crossover(mother, father, 25)
    print("OURS: head of the mother, then the missing flowers in the father's order")
    print(f"  length            : {len(child)}")
    print(f"  distinct flowers  : {len(set(child.tolist()))} / 50")


def demo_mutation():
    """Slide 10: count the links of the tour each mutation breaks."""
    def links(order):
        steps = ["hive"] + list(order) + ["hive"]
        return {frozenset(pair) for pair in zip(steps, steps[1:])}

    tour = list(range(10))
    swapped = tour.copy()
    swapped[2], swapped[7] = swapped[7], swapped[2]
    reversed_ = tour[:2] + tour[2:8][::-1] + tour[8:]

    print(f"tour     : {tour}")
    print(f"swap     : {swapped}   links broken: {len(links(tour) - links(swapped))}")
    print(f"reverse  : {reversed_}   links broken: {len(links(tour) - links(reversed_))}")


DEMOS = {"brute": demo_brute, "speed": demo_speed,
         "crossover": demo_crossover, "mutation": demo_mutation}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in DEMOS:
        print("usage: uv run python demo.py [" + " | ".join(DEMOS) + "]")
        sys.exit(1)
    DEMOS[sys.argv[1]]()
