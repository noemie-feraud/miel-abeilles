"""Honey and bees: the flower field and trip length computation."""

import numpy as np
from config import BEEHIVE_POSITION
from bee import Bee
from config import NB_BEES
from config import BEEHIVE_POSITION, NB_BEES, NB_ELITES, TOURNAMENT_SIZE, MUTATION_RATE 


def load_field(path):
    """read the flower file and return an (n, 2) array of coordinates"""
    data = np.genfromtxt(path, delimiter=',', skip_header=1, dtype=float)
    if data.ndim != 2 or data.shape[1] != 2:
        raise ValueError(f"Expected 2 columns, got shape{data.shape}")
    if np.isnan(data).any():
        raise ValueError(f"Unreadable coordinates in {path}")
    return data

def build_distance_matrix(flowers):
    """Pre-compute the distance between every pair of points. 
    Index 0 is the hive, indices 1..n are the flowwers.
    Returns an (n+1, n+1) array
    """
    points = np.vstack([BEEHIVE_POSITION, flowers])
    deltas = points[:, None, :] - points[None, :, :]
    return np.sqrt((deltas ** 2).sum(axis=2))

def path_length(order, distances):
    """Total length of hive -> flowers in the given order -> hive.

    `order` is a permutation of 0..n-1 (flower numbers).
    Row 0 of `distances` is the hive, so flower i sits at index i + 1.
    """
    steps = np.empty(len(order) + 2, dtype=np.int64)
    steps[0] = 0
    steps[1:-1] = np.asarray(order) + 1
    steps[-1] = 0
    return distances[steps[:-1], steps[1:]].sum()

def crossover(order_a, order_b, cut):
    """take the head of A, then the missing flowers in B's order. Always
    a valid permutation"""
    head = order_a[:cut]
    taken = np.zeros(len(order_a), dtype=bool)
    taken[head] = True
    tail = order_b[~taken[order_b]]
    return np.concatenate([head, tail])

def mutate_swap(order, rng):
    """Swap two flowers. Simple, but breaks 
    four edges of the tour"""
    child = order.copy()
    i, j = rng.choice(len(order), size=2, replace=False)
    child[i], child[j] = child[j], child[i]
    return child

def mutate_reverse(order, rng):
    """Reverse a random segment (2-opt move). Breaks only two
    edges."""
    child = order.copy()
    i, j = sorted(rng.choice(len(order) + 1, size=2, replace=False))
    child[i:j] = child[i:j][::-1]
    return child

def tournament(bees, rng, size):
    """Pick 'size bees at random, return the best of them"""
    contenders = rng.choice(len(bees), size=size, replace=False)
    return min(bees[i] for i in contenders)

class Beehive:
    """Owns the flower field, the distance matrix, and the colony."""
    def __init__(self, flowers, seed=None):
        self.flowers = flowers
        self.nb_flowers = len(flowers)
        self.distances = build_distance_matrix(flowers)
        self.bees = []
        self.history = []
        self.rng = np.random.default_rng(seed)

    def init_bee(self):
        """One bee with a random visiting order"""
        order = self.rng.permutation(self.nb_flowers)
        return Bee(order, path_length(order, self.distances))

    def init_bees(self):
        """Build the starting colony, best bee first"""
        self.bees = [self.init_bee() for _ in range(NB_BEES)]
        self.bees.sort()
        self.record()

    def next_generation(self):
        """Replace the colony by the elite plus their offdpring."""
        new_bees = self.bees[:NB_ELITES]
        while len (new_bees) <NB_BEES:
            mother = tournament(self.bees, self.rng, TOURNAMENT_SIZE)
            father = tournament(self.bees, self.rng, TOURNAMENT_SIZE)
            cut = int(self.rng.integers(1, self.nb_flowers))
            order = crossover(mother.order, father.order, cut)
            if self.rng.random() < MUTATION_RATE:
                order = mutate_reverse(order, self.rng)
            new_bees.append(Bee(order, 
                                path_length(order, self.distances),
                                parents=(mother.id, father.id)))
        self.bees = sorted(new_bees)
        self.record()

    def average_distance(self):
        return sum(bee.distance for bee in self.bees) / len(self.bees)

    def record(self):
        """Append (average, best) of the current colony to the history"""
        self.history.append((self.average_distance(),
self.bees[0].distance))
        
    def print_average_distance(self):
        print(f"{self.average_distance():.0f}")

    def __str__(self):
        return f"Beehive: {self.nb_flowers} flowers, {len(self.bees)} bees"


    