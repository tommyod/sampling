import random
import math
from sampling.cumsum import CumulativeSum
import numbers
from collections.abc import Iterator, Hashable
from abc import abstractmethod


class WeightedUrn(Iterator):
    def __init__(self, population, weights):
        self._population = list(population)
        self._weights = list(weights)

        if len(self._population) != len(self._weights):
            raise ValueError("'population' and 'weights' must have same length")

        if not all(isinstance(e, Hashable) for e in self._population):
            raise TypeError("elements of population must be hashable.")
        if len(self._population) != len(set(self._population)):
            raise ValueError("population must contain unique elements.")

        if all(w >= 0 for w in self._weights):
            self._cumulative_sum_object = CumulativeSum(self._weights)
        else:
            raise ValueError("all weights must be greater than or equal to zero.")

    def __iter__(self):
        return self

    def __bool__(self):
        return self.size() > 0

    def __contains__(self, value):
        return value in self._population

    def update_weight(self, index, value):
        if value < 0:
            raise ValueError("'value' must be greater than or equal to zero.")

        if isinstance(index, numbers.Integral):
            self._cumulative_sum_object.update_weight(index, value)
        else:
            raise TypeError("'index' must be an integer")

    def extend(self, elements, weights):
        new_elements = list(elements)
        if len(new_elements) != len(set(new_elements)):
            raise ValueError("all elements in new population must be unique.")
        if all(isinstance(e, Hashable) for e in new_elements):
            self._population.extend(new_elements)
        else:
            raise TypeError("one or more values in 'elements' unhashable.")

        new_weights = list(weights)
        if all(w >= 0 for w in new_weights):
            self._cumulative_sum_object.extend(new_weights)
        else:
            raise ValueError("all weights must be greater than or equal to zero.")

    def add(self, element, weight):
        self.extend([element], [weight])

    def remove(self, element):
        try:
            index = self._population.index(element)
        except ValueError:
            raise ValueError(f"element {element} not in population.")
        self._population.pop(index)
        self._cumulative_sum_object.remove(index)

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def size(self):
        pass


class WeightedFiniteUrn(WeightedUrn):
    def __repr__(self):
        return type(self).__name__

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


class WeightedInfiniteUrn(WeightedUrn):
    def __repr__(self):
        return type(self).__name__

    def __next__(self):
        if self.size() == 0:
            raise StopIteration

        pick = random.random() * self._cumulative_sum_object.get_sum()
        index = self._cumulative_sum_object.query(pick)
        return self._population[index]

    def size(self):
        # TODO: Think about what size of an infinite urn should mean
        return float("inf")


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
        population.extend(self._population)
        self._population = population
        self._num_remaining = len(self._population)

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
    try:
        # Weighted urns
        if weights:
            if replace:
                return WeightedInfiniteUrn(population, weights)
            else:
                return WeightedFiniteUrn(population, weights)
        # Unweighted urns
        else:
            if replace:
                return UnweightedInfiniteUrn(population)
            else:
                return UnweightedFiniteUrn(population)
    except Exception as e:
        raise e
