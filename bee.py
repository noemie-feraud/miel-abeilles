"""A bee: one candidate visiting order for the flowers in the field."""

import numpy as np

class Bee:
    """A bee is one visiting order of the flowers, plus its trip length."""

    _counter = 0

    def __init__(self, order, distance, parents=(None, None)):
        Bee._counter += 1
        self.id = Bee._counter
        self.order = np.array(order, dtype=np.int64)
        self.distance = float(distance)
        self.parents = tuple(parents)
    def __repr__(self):
        return f"Bee#{self.id}({self.distance:.0f})"

    def __lt__(self, other):
        return self.distance < other.distance

