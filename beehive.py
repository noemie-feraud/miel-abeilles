"""Honey and bees: the flower field and trip length computation."""

import numpy as np
from config import BEEHIVE_POSITION


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