import random
from collections.abc import Sequence
import math
import itertools
import bisect


class Urn:
    def __init__(self, population, replace=False, weights=None):

        # Check if our population is indexable
        if isinstance(population, Sequence):
            self.population = population.copy()
            # if the population is not indexable, try to convert to an indexable datastructure
            try:
                self.population = list(population)
            except TypeError:
                print(f"{type(population)} is not supported")
                return

        # Store urn classification
        self.replace = replace
        self.weights = weights
        self.num_remaining = len(self.population)

    def __iter__(self):
        return self

    def __next__(self):

        # Get next element in a collection of weighted elements
        if self.replace and self.weights:
            # Accumulate the weights for the population
            weights = list(itertools.accumulate(self.weights))
            # Get a random weight within the weight distribution
            choice = weights[-1] * random.random()
            # Find the index the random weight corresponds to
            index = bisect.bisect_left(weights, choice)
            return self.population[index]

        # Get next element in a collection of unweighted elements
        elif self.replace and not self.weights:
            # Get a random index within the boundaries of our collection
            index_choice = math.floor(random.random() * len(self.population))
            return self.population[index_choice]

        elif not self.replace and self.weights:
            pass

        # Get next element in a collection of unweighted elements without replace
        # We implement the Fisher-Yates shuffle (1938)
        # See https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle
        # This is the implementation of the modern method (Richard Durstenfeld, 1964)
        elif not self.replace and not self.weights:

            if self.num_remaining == 0:
                raise StopIteration
            self.num_remaining -= 1

            # generate a random number in [0, num_remaining]
            pick = math.floor(random.random() * (self.num_remaining + 1))

            # Move our pick to the last index within current range, return it
            self.population[self.num_remaining], self.population[pick] = (
                self.population[pick],
                self.population[self.num_remaining],
            )
            return self.population[self.num_remaining]
