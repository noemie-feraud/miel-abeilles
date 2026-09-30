"""Project-wide constants, all imposed by the assignment."""

# The hive: start and end of every trip.
BEEHIVE_POSITION = (500.0, 500.0)

# Colony size: 100 foragers, plus the queen kept apart.
NB_BEES = 100

# Where the flower coordinates live.
FLOWERS_PATH = "data/flowers.csv"

# How many generations to run.
NB_GENERATIONS = 100

# Genetic algorithm parameters.
NB_ELITES = 10          # best bees carried over untouched
TOURNAMENT_SIZE = 20
MUTATION_RATE = 0.7    # probability of mutating a newborn
