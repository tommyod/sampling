import math


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
                current_index = self._left_child(current_index)

            # go right down the tree
            else:
                search_weight -= self.bst[current_index]
                current_index = self._right_child(current_index)

        return current_index - self.leaf_nodes

    def update_weight(self, index, weight):
        # Set leaf to new weight
        index = index + self.leaf_nodes
        self.bst[index] = weight

        # Set parent left and right sums
        prev = index
        curr = self._parent(prev)

        # Parent of a left child
        if prev % 2 == 0:
            self.bst[curr] = weight
        else:
            self.right_sums[curr] = weight

        # Move one tree level up
        curr, prev = self._parent(curr), curr
        while curr >= 1:
            # We came from the left
            if prev % 2 == 0:
                self.bst[curr] = self.bst[prev] + self.right_sums[prev]
            # We came from the right
            else:
                self.right_sums[curr] = self.bst[prev] + self.right_sums[prev]
            # Move one tree level up
            curr, prev = self._parent(curr), curr

    def __getitem__(self, index):
        return self.bst[self.leaf_nodes + index]
