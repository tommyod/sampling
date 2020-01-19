import random

# from collections.abc import Sequence
import math
import itertools
import bisect
from sampling.tree import CumulativeSumTree

from collections.abc import Iterator, Sized


class Urn(Iterator, Sized):
    """A base class for an Urn. """

    def __init__(self, population, replace=False, weights=None):
        """Initialize Urn.

            Parameters
            ----------

            population : Sequence
                An indexable, iterable (mutable) sequence of elements
            replace : bool
                Whether or not the population is replaced (default False)
            weights : Sequence
                An indexable, iterable (mutable) sequence of weights corresponding to population (default None)
        """

        # TODO: Refine data type
        self.population = list(population)

        # Store urn parameters
        self.replace = replace
        self.weights = weights
        self.num_remaining = len(self.population)

        if not self.replace and self.weights:
            self.cumulative_sum_tree = CumulativeSumTree(self.weights)

    def __iter__(self):
        """Initialize iter."""
        return self

    def __len__(self):
        if self.replace:
            return float("inf")
        else:
            return self.num_remaining

    def __bool__(self):
        return len(self) > 0

    def __contains__(self, value):
        raise NotImplementedError

    def __next__(self):
        """Return next element in population based on urn parameters."""

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
            if self.num_remaining == 0:
                raise StopIteration
            self.num_remaining -= 1

            pick = random.random() * self.cumulative_sum_tree.get_sum()
            index = self.cumulative_sum_tree.query(pick)
            self.cumulative_sum_tree.update_weight(index, 0)
            return self.population[index]

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
