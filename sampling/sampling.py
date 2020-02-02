import random
import math
import itertools
import bisect
from sampling.tree import CumulativeSumTree

from collections.abc import Iterator


class Urn(Iterator):
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
        self._population = list(population)

        # Store urn parameters
        self.replace = replace
        self._weights = weights

        self._num_remaining = float("inf") if self.replace else len(self._population)

        if not self.replace and self._weights:
            self.cumulative_sum_tree = CumulativeSumTree(self._weights)

    def __iter__(self):
        return self

    def size(self):
        return self._num_remaining

    def __bool__(self):
        return self.size() > 0

    def __contains__(self, value):
        raise NotImplementedError

    def __next__(self):
        """Return next element in population based on urn parameters."""

        # -------------- WEIGHTED SAMPLING WITH REPLACEMENT -------------------
        # Get next element in a collection of weighted elements
        if self.replace and self._weights:
            # Accumulate the weights for the population
            weights = list(itertools.accumulate(self._weights))
            # Get a random weight within the weight distribution
            choice = weights[-1] * random.random()
            # Find the index the random weight corresponds to
            index = bisect.bisect_left(weights, choice)
            return self._population[index]

        # -------------- UNWEIGHTED SAMPLING WITH REPLACEMENT -----------------
        # Get next element in a collection of unweighted elements
        elif self.replace and not self._weights:
            # Get a random index within the boundaries of our collection
            index_choice = math.floor(random.random() * len(self._population))
            return self._population[index_choice]

        # -------------- WEIGHTED SAMPLING WITHOUT REPLACEMENT ----------------
        elif not self.replace and self._weights:
            if self._num_remaining == 0:
                raise StopIteration
            self._num_remaining -= 1

            pick = random.random() * self.cumulative_sum_tree.get_sum()
            index = self.cumulative_sum_tree.query(pick)
            self.cumulative_sum_tree.update_weight(index, 0)
            return self._population[index]

        # -------------- UNWEIGHTED SAMPLING WITH REPLACEMENT -----------------
        # Get next element in a collection of unweighted elements without replace
        # We implement the Fisher-Yates shuffle (1938)
        # See https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle
        # This is the implementation of the modern method (Richard Durstenfeld, 1964)
        elif not self.replace and not self._weights:

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


def sample(population, size=1, replace=False, weights=None):
    """
    Draw samples from a collection.
    
    Parameters
    ----------
    population: list
        The data points. 
    
    replace: bool
        Sample with or without replacement.
        
    weights: list
        One weight per data point. If None is
        passed, uniform weights are used.
        
    Returns
    -------
    list
    Returns a new list of length size containing elements from the population 
    while leaving the original population unchanged.
        
        
    Examples
    --------
    >>> data = [1, 3, 4, 7]
    >>> weights = [3, 4, 2, 1]
    >>> sample(data, replace=False, weights=weights)
    >>> sample(data, replace=False, weights=None)
    
    """
    urn = Urn(population=population, replace=replace, weights=weights)
    return list(itertools.islice(urn, size))


if __name__ == "__main__":
    """
    tree = CumulativeSumTree([0.2, 0.3, 0.1, 0.4, 0.8])
    print(tree.bst)
    print(tree.right_sums)
    print(tree.query(0.55))
    print(tree.query(0.61))
    for _ in range(100):
        weight = random.random() * tree.get_sum()
        i = tree.query(weight)
        left_sum = sum(tree[j] for j in range(100) if j < i)
        assert left_sum < weight
        assert left_sum + tree[i] > weight
    """

    size = 8
    weights = [i * 0.1 for i in range(size)]
    indices = []

    tree = CumulativeSumTree(weights)
    for _ in range(size):
        weight = random.random() * tree.get_sum()
        i = tree.query(weight)
        # print(i)
        # print(tree.bst)
        # print(tree.right_sums)
        indices.append(i)
        tree.update_weight(i, 0)

    assert len(indices) == len(set(indices))
    # print(tree.bst)
    # print(tree.right_sums)
    # print(tree.query(0.55))
