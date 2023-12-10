class Node:
    def __init__(self, node_value, node_type):
        self.node_type = node_type
        self.node_value = node_value  # The value put inside the node (if exists)
        self.children: list = []  # List of Nodes
        self.sibling = None  # Sibling Node if Exists
        self.is_errored: bool = False  # To raise error on GUI if Error occurred

    def add_child(self, node):
        self.children.append(node)
