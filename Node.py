class Node:
    def __init__(self, tokens=None):
        self.tokens = tokens
        self.neighbor = None
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def add_neighbor(self, node):
        self.neighbor = node
