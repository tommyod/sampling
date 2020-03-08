import random
import math
import itertools
import bisect
from sampling.cumsum import CumulativeSum
import numbers
from collections.abc import Iterator, Hashable


class WeightedFiniteUrn(Iterator):
    def __init__(self, population, weights):
        # TODO: Better error messages
        assert not isinstance(population, set)
        assert not isinstance(weights, set)

        self._population = list(population)
        assert all(isinstance(e, Hashable) for e in self._population)
        assert len(self._population) == len(set(self._population))

        _weights = list(weights)
        assert all(w >= 0 for w in _weights)

        self._cumulative_sum_object = CumulativeSum(_weights)

    def __repr__(self):
        return type(self).__name__

    def __iter__(self):
        return self

    def __bool__(self):
        return self.size() > 0

    def __contains__(self, value):
        return value in self._population

    def __next__(self):
        if self.size() == 0:
            raise StopIteration

        pick = random.random() * self._cumulative_sum_object.get_sum()
        index = self._cumulative_sum_object.query(pick)
        value = self._population[index]
        self.remove(value)
        return value

    def size(self):
        return len(self._population)

    def update_weight(self, index, value):
        if not isinstance(index, numbers.Integral):
            raise TypeError("'index' must be an integer")
        assert value >= 0  # TODO: Proper type check
        self._cumulative_sum_object.update_weight(index, value)

    def extend(self, elements, weights):
        assert not isinstance(elements, set)
        assert not isinstance(weights, set)
        _elements = list(elements)
        self._population.extend(_elements)
        assert all(isinstance(e, Hashable) for e in _elements)
        assert len(_elements) == len(set(_elements))

        self._cumulative_sum_object.extend(weights)

    def add(self, element, weight):
        self.extend([element], [weight])

    def remove(self, element):
        index = self._population.index(element)
        self._population.pop(index)
        self._cumulative_sum_object.remove(index)


class WeightedInfiniteUrn(Iterator):
    def __init__(self, population, weights):
        # TODO: Better error messages
        assert not isinstance(population, set)
        assert not isinstance(weights, set)

        self._population = list(population)
        assert all(isinstance(e, Hashable) for e in self._population)
        assert len(self._population) == len(set(self._population))

        _weights = list(weights)
        assert all(w >= 0 for w in _weights)

        self._cumulative_sum_object = CumulativeSum(_weights)

    def __repr__(self):
        return type(self).__name__

    def __iter__(self):
        return self

    def __bool__(self):
        return self.size() > 0

    def __contains__(self, value):
        return value in self._population

    def __next__(self):
        if self.size() == 0:
            raise StopIteration

        pick = random.random() * self._cumulative_sum_object.get_sum()
        index = self._cumulative_sum_object.query(pick)
        return self._population[index]

    def size(self):
        # TODO: Think about what size of an infinite urn should mean
        return float("inf")

    def update_weight(self, index, value):
        if not isinstance(index, numbers.Integral):
            raise TypeError("'index' must be an integer")
        assert value >= 0  # TODO: Proper type check
        self._cumulative_sum_object.update_weight(index, value)

    def extend(self, elements, weights):
        assert not isinstance(elements, set)
        assert not isinstance(weights, set)
        _elements = list(elements)
        self._population.extend(_elements)
        assert all(isinstance(e, Hashable) for e in _elements)
        assert len(_elements) == len(set(_elements))

        self._cumulative_sum_object.extend(weights)

    def add(self, element, weight):
        self.extend([element], [weight])

    def remove(self, element):
        index = self._population.index(element)
        self._population.pop(index)
        self._cumulative_sum_object.remove(index)


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
        return value in self._population[: self._num_remaining]

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

    def add(self, element):
        # TODO: Better checking
        self.extend([element])

    def remove(self, element):
        i = self._population[: self._num_remaining].index(element)
        self._population.pop(i)
        self._num_remaining -= 1


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
        # TODO: Think about what size of an infinite urn should mean
        return float("inf")

    def extend(self, population):
        self._population.extend(list(population))

    def add(self, element):
        # TODO: Better checking
        self.extend([element])

    def remove(self, element):
        i = self._population.index(element)
        self._population.pop(i)


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
