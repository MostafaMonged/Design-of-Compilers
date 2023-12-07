class Node:
    def __init__(self, node_value, node_type):
        self.node_type = node_type
        self.node_value = node_value   # The value put inside the node (if exists)
        self.__children: list = []     # List of Nodes
        self.sibling = None            # Sibling Node if Exists
        self.is_errored: bool = False  # To raise error on GUI if Error occurred

    def add_child(self, node):
        self.__children.append(node)


read_node = Node("x", "READ")
if_node = Node("", "IF")
read_node.sibling = if_node
op_node = Node("<", "OP")
id1_node = Node("x", "IDENTIFIER")
const1_node = Node("0", "NUMBER")
op_node.add_child(const1_node)
op_node.add_child(id1_node)
if_node.add_child(op_node)
assign_fact_node = Node("fact", "ASSIGN")
const2_node = Node("1", "NUMBER")
assign_fact_node.add_child(const2_node)
if_node.add_child(assign_fact_node)
repeat_node = Node("", "REPEAT")
assign_fact_node.sibling = repeat_node
assign_fact_node2 = Node("fact", "ASSIGN")
repeat_node.add_child(assign_fact_node2)
assign_x_node = Node("x", "ASSIGN")
assign_fact_node2.sibling = assign_x_node
op_node2 = Node("*", "OP")
id2_node = Node("fact", "IDENTIFIER")
id3_node = Node("x", "IDENTIFIER")
op_node2.add_child(id2_node)
op_node2.add_child(id3_node)
assign_fact_node2.add_child(op_node2)
op_node3 = Node("-", "OP")
id4_node = Node("x", "IDENTIFIER")
const3_node = Node("1", "NUMBER")
op_node3.add_child(id4_node)
op_node3.add_child(const3_node)
assign_x_node.add_child(op_node3)
op_node4 = Node("=", "OP")
id5_node = Node("x", "IDENTIFIER")
const4_node = Node("0", "NUMBER")
op_node4.add_child(id5_node)
op_node4.add_child(const4_node)
repeat_node.add_child(op_node4)
write_node = Node("", "WRITE")
repeat_node.sibling = write_node
id6_node = Node("fact", "IDENTIFIER")
write_node.add_child(id6_node)
