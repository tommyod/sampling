# import heapq
import operator


class LevelTree:
    def __init__(self, root):
        self._root = root
        self.level_nodes = [[self._root]]

    def add(self, node):

        for level, nodes in enumerate(self.level_nodes):
            print(f"Current level: {level}")
            min_node = min(nodes, key=operator.attrgetter("weight"))
            print(min_node)
            max_node = max(nodes, key=operator.attrgetter("weight"))
            print(max_node)

            if node.weight > max_node.weight:
                if max_node is self._root:
                    self._root = node
                new_min = "REMOVE"  # pass
                if max_node.left:
                    pass

            # Copy references from node we displace
            node.parent = min_node.parent
            node.left_child = min_node.left_child
            node.right_child = min_node.right_child
            node = min_node

        if node:
            self.insert_at_subroot(self._root, node)
            # levels.append([node])

    def insert_at_subroot(self, subroot_node, node):
        if not subroot_node.left_child:
            subroot_node.left_descendants += 1
            subroot_node.left_child = node
            node.parent = subroot_node
            # TODO: Update weights recursively up in the tree
            return
        if not subroot_node.right_child:
            subroot_node.right_descendants += 1
            subroot_node.right_child = node
            node.parent = subroot_node
            # TODO: Update weights recursively up in the tree
            return
        if subroot_node.left_descendants > subroot_node.right_descendants:
            self.insert_at_subroot(subroot_node.right_child, node)
        else:
            self.insert_at_subroot(subroot_node.left_child, node)

            if node.weight <= min_node.weight:
                if len(nodes) >= 2 ** level:
                    continue
                else:
                    pass

        # pass


class Node:
    def __init__(self, obj, weight, parent=None, left_child=None, right_child=None):
        self.obj = obj
        self.weight = weight
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.left_descendants = 0
        self.right_descendants = 0
        self.left_sum = 0
        self.right_sum = 0

    def update_left_sum(self):
        """ Update left sum with (updated) variables from left child """
        if self.left_child:
            self.left_sum = self.left_child.left_sum + self.left_child.right_sum + self.left_child.weight
        else:
            self.left_sum = 0

    def update_right_sum(self):
        """ Update right sum with (updated) variables from right child """
        if self.right_child:
            self.right_sum = self.right_child.left_sum + self.right_child.right_sum + self.right_child.weight
        else:
            self.right_sum = 0

    def __repr__(self):
        return f"Node(obj={self.obj}, weight={self.weight})"


node = Node(0, 9)
tree = LeveledTree(node)
node2 = Node(1, 14)
tree.add(node2)
