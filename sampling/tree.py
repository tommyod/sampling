import math


class CumulativeSumTree:
    def __init__(self, weights):
        self.weights = list(weights)
        if any(w < 0 for w in weights):
            raise ValueError("all weights must be greater than or equal to zero.")

        self.leaf_nodes = int(2 ** math.ceil(math.log(len(weights), 2)))
        self.right_sums = [0] * self.leaf_nodes
        self.bst = self._initialise_bst()
        self._build_tree()

    def _initialise_bst(self):
        bst = [0] * self.leaf_nodes
        bst.extend(self.weights)
        bst.extend((self.leaf_nodes - len(self.weights)) * [0])
        return bst

    def _build_tree(self):
        nodes_in_level = self.leaf_nodes // 2

        while nodes_in_level > 0:
            # Loop over every node at this level in the tree
            for node in range(nodes_in_level, nodes_in_level * 2):
                # Get indices of children
                left_child_index = self._left_child(node)
                right_child_index = self._right_child(node)

                # Recursively set the sums
                if self._is_leaf(left_child_index):
                    self.bst[node] = self.bst[left_child_index]
                    self.right_sums[node] = self.bst[right_child_index]
                else:
                    self.bst[node] = (
                        self.bst[left_child_index] + self.right_sums[left_child_index]
                    )
                    self.right_sums[node] = (
                        self.bst[right_child_index] + self.right_sums[right_child_index]
                    )

            # Go up one level in the tree
            nodes_in_level = nodes_in_level // 2

    def _is_leaf(self, idx):
        return idx >= self.leaf_nodes

    def _left_child(self, idx):
        return 2 * idx

    def _right_child(self, idx):
        return 2 * idx + 1

    def _parent(self, idx):
        return idx // 2

    def get_sum(self):
        return self.bst[1] + self.right_sums[1]

    def query(self, search_weight):
        if not 0 <= search_weight <= self.get_sum():
            raise ValueError(f"queried weight must be between 0 and {self.get_sum()}")

        current_index = 1

        while not self._is_leaf(current_index):
            # Go left down the tree
            if search_weight <= self.bst[current_index]:
                current_index = self._left_child(current_index)
            # Go right down the tree
            else:
                search_weight -= self.bst[current_index]
                current_index = self._right_child(current_index)

        return current_index - self.leaf_nodes

    def update_weight(self, index, weight):
        # Set leaf to new weight
        index = index + self.leaf_nodes
        self.bst[index] = weight

        # Set parent left and right sums
        previous = index
        current = self._parent(previous)

        # Parent of a left child
        if previous % 2 == 0:
            self.bst[current] = weight
        else:
            self.right_sums[current] = weight

        # Move one tree level up
        current, previous = self._parent(current), current
        while current >= 1:
            # We came from the left
            if previous % 2 == 0:
                self.bst[current] = self.bst[previous] + self.right_sums[previous]
            # We came from the right
            else:
                self.right_sums[current] = (
                    self.bst[previous] + self.right_sums[previous]
                )
            # Move one tree level up
            current, previous = self._parent(current), current

    def __getitem__(self, index):
        return self.bst[self.leaf_nodes + index]
