from Node import Node


class Parser:
    def __init__(self):
        self.tokens_list = []
        self.index = 0
        self.error_flag = 0

    def match(self, parameter_from_grammar):
        if self.tokens_list[self.index] == parameter_from_grammar:
            self.index += 1
        else:
            print("Error, the next token input is not matching the grammar rules!")
            self.error_flag = 1

    def another_code(self, scanner_output):
        self.tokens_list = scanner_output
        self.index = 0

    def parse(self):  # will contain the first procedure of grammar to start the program parsing
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

        return read_node
