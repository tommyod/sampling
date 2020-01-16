import random

# from collections.abc import Sequence
import math
import itertools
import bisect


class Urn:
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

    def __iter__(self):
        """Initialize iter."""
        return self

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


class CumulativeSumTree:
    def __init__(self, weights):
        self.leaf_nodes = int(2 ** math.ceil(math.log(len(weights), 2)))
        self.bst = [0] * self.leaf_nodes
        self.bst.extend(weights)
        self.bst.extend((self.leaf_nodes - len(weights)) * [0])
        self.right_sums = [0] * self.leaf_nodes

        nodes_in_level = self.leaf_nodes // 2
        while nodes_in_level > 0:
            # loop over every node at this level in the tree
            for i in range(nodes_in_level, nodes_in_level * 2):

                # Get indices of children
                left_child_index = self._left_child(i)
                right_child_index = self._right_child(i)

                # recursively set the sums
                if self._is_leaf(left_child_index):
                    self.bst[i] = self.bst[left_child_index]
                    self.right_sums[i] = self.bst[right_child_index]
                else:
                    self.bst[i] = self.bst[left_child_index] + self.right_sums[left_child_index]
                    self.right_sums[i] = self.bst[right_child_index] + self.right_sums[right_child_index]

            # go up one level in the tree
            nodes_in_level = nodes_in_level // 2

    def _is_leaf(self, i):
        return i >= self.leaf_nodes

    def _left_child(self, i):
        return 2 * i

    def _right_child(self, i):
        return 2 * i + 1

    def _parent(self, i):
        return i // 2

    def get_sum(self):
        return self.bst[1] + self.right_sums[1]

    def query(self, search_weight):
        assert 0 <= search_weight <= self.get_sum()

        current_index = 1

        while not self._is_leaf(current_index):
            # go left down the tree
            if search_weight <= self.bst[current_index]:
                # search_weight -= self.bst[current_index]
                current_index = self._left_child(current_index)

            # go right down the tree
            else:
                search_weight -= self.bst[current_index]
                current_index = self._right_child(current_index)

        return current_index - self.leaf_nodes

    def __getitem__(self, index):
        return self.bst[self.leaf_nodes + index]


if __name__ == "__main__":
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
