"""Le miel et les abeilles : le champ de fleurs et le calcul des trajets."""

import numpy as np

# La ruche est imposée par l'énoncé. Point de départ et d'arrivée de chaque abeille.
HIVE = (500.0, 500.0)


def load_field(path):
    """Lit le fichier des fleurs et renvoie un tableau (n, 2) de coordonnées."""
    data = np.genfromtxt(path, delimiter=",", skip_header=1, dtype=float)
    data = data.reshape(-1, 2)
    if np.isnan(data).any():
        raise ValueError(f"Coordonnees illisibles dans {path}")
    return data


def build_distance_matrix(flowers):
    """Pre-calcule la distance entre chaque paire de points.

    L'indice 0 est la ruche, les indices 1..n sont les fleurs.
    """
    points = np.vstack([HIVE, flowers])
    ecarts = points[:, None, :] - points[None, :, :]
    return np.sqrt((ecarts ** 2).sum(axis=2))


def path_length(order, distances):
    """Longueur du trajet ruche -> fleurs dans l'ordre donne -> ruche."""
    etapes = np.empty(len(order) + 2, dtype=int)
    etapes[0] = 0
    etapes[1:-1] = order
    etapes[-1] = 0
    return distances[etapes[:-1], etapes[1:]].sum()
