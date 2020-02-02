import random
import math
import itertools
import bisect
from sampling.tree import CumulativeSumTree
import numbers

from collections.abc import Iterator


class WeightedFiniteUrn(Iterator):
    def __init__(self, population, weights):
        self._population = list(population)
        self._weights = list(weights)
        self._num_remaining = len(self._population)
        self._cumulative_sum_tree = CumulativeSumTree(self._weights)

    def __repr__(self):
        return type(self).__name__

    def __iter__(self):
        return self

    def __bool__(self):
        return self.size() > 0

    def __contains__(self, value):
        # TODO: Implement
        raise NotImplementedError

    def __next__(self):
        if self._num_remaining == 0:
            raise StopIteration
        self._num_remaining -= 1

        pick = random.random() * self._cumulative_sum_tree.get_sum()
        index = self._cumulative_sum_tree.query(pick)
        self._cumulative_sum_tree.update_weight(index, 0)
        return self._population[index]

    def size(self):
        return self._num_remaining

    def update_weight(self, index, value):
        if not isinstance(index, numbers.Integral):
            raise TypeError("'index' must be an integer")
        assert value >= 0 #TODO: Proper type check
        self._cumulative_sum_tree.update_weight(index, value)


class WeightedInfiniteUrn(Iterator):
    def __init__(self, population, weights):
        self._population = list(population)
        self._weights = list(weights)
        self._cumulative_weights = list(itertools.accumulate(self._weights))

    def __repr__(self):
        return type(self).__name__

    def __iter__(self):
        return self

    def __bool__(self):
        return len(self._population) > 0

    def __contains__(self, value):
        # TODO: Implement this 
        raise NotImplementedError

    def __next__(self):
        # Get a random weight within the weight distribution
        choice = self._cumulative_weights[-1] * random.random()
        # Find the index the random weight corresponds to
        index = bisect.bisect_left(self._cumulative_weights, choice)
        return self._population[index]

    def size(self):
        return float("inf")

    def update_weight(self, index, value):
        """ TODO: Implement """
        raise NotImplementedError



class UnweightedFiniteUrn(Iterator):
    def __init__(self, population):
        self._population = list(population)
        self._num_remaining = len(self._population)

    def __repr__(self):
        return type(self).__name__

    def __iter__(self):
        return self

    def __bool__(self):
        return self.size() > 0

    def __contains__(self, value):
        return value in self._population[:self._num_remaining]

    def __next__(self):
        if self._num_remaining == 0:
            raise StopIteration
        self._num_remaining -= 1

        # generate a random number in [0, num_remaining]
        pick = math.floor(random.random() * (self._num_remaining + 1))

        # Move our pick to the last index within current range, return it
        self._population[self._num_remaining], self._population[pick] = (
            self._population[pick],
            self._population[self._num_remaining],
        )
        return self._population[self._num_remaining]

    def size(self):
        return self._num_remaining

    def extend(self, population):
        population = list(population)
        extra_length = len(population)
        population.extend(self._population)
        self._population = population
        self._num_remaining += extra_length


class UnweightedInfiniteUrn(Iterator):
    def __init__(self, population):
        self._population = list(population)
        self._num_remaining = float("inf")

    def __repr__(self):
        return type(self).__name__

    def __iter__(self):
        return self

    def __bool__(self):
        return len(self._population) > 0

    def __contains__(self, value):
        return value in self._population

    def __next__(self):
        # Get a random index within the boundaries of our collection
        index_choice = math.floor(random.random() * len(self._population))
        return self._population[index_choice]

    def size(self):
        return float("inf")

    def extend(self, population):
        self._population.extend(list(population))


def Urn(population, replace=False, weights=None):
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

    if replace and weights:
        return WeightedInfiniteUrn(population, weights)
    elif not replace and weights:
        return WeightedFiniteUrn(population, weights)
    elif replace and weights is None:
        return UnweightedInfiniteUrn(population)
    elif not replace and weights is None:
        return UnweightedFiniteUrn(population)
    else:
        # TODO: Raise proper exception
        raise Exception
