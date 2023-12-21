from Node import Node

class Parser:
    def __init__(self):
        self.tokens_list = []
        self.index = 0
        self.error_flag = 0
        self.OP = ["+", "-", "*", "/", "<", "="]

    def match(self, parameter_from_grammar):
        if self.tokens_list[self.index][0] == parameter_from_grammar:#edit
            self.index += 1
        else:
            print("Error, the next token input is not matching the grammar rules!")
            self.error_flag = 1

    def another_code(self, scanner_output):
        self.tokens_list = scanner_output
        self.index = 0

    def current_token(self):
            return self.tokens_list[self.index][0] if self.index < len(self.tokens_list) else None
    
    def previous_token(self):
        return self.tokens_list[self.index - 1][0] if self.index > 0 else None

    def next_token(self):
        return self.tokens_list[self.index + 1][0] if self.index < len(self.tokens_list) - 1 else None

    def token_type(self):
        return self.tokens_list[self.index][1] if self.index < len(self.tokens_list) else None

    # def parse(self):  # will contain the first procedure of grammar to start the program parsing
    #     # program()
    #     pass


    #============= starting the grammar procedures ==================
    def program(self):
        root = self.stmt_sequence()
        if self.current_token() is not None:
            print("program has syntax error")
            error = Node("ERRORRRR", "ERROR")
            error.is_errored = True
            temp = root
            while temp.sibling is not None:
                temp = temp.sibling
            temp.sibling = error
        return root
    
    def assign_stmt(self):
        assign_node = Node("ERRORRRR", "ASSIGN")
        if(str(self.token_type()) == "IDENTIFIER"):
            self.match(self.current_token()) # x := 2 , read := 2
            if(self.current_token() == ":="):
                assign_node.node_value = str(self.previous_token()) #which is the identifier of the Assign node
                self.match(":=")
                assign_node.add_child(self.exp())
            else: 
                assign_node.is_errored = True
                print(self.current_token())
        else: 
            assign_node.is_errored = True
            print(str(self.token_type()))
            print(self.tokens_list)
        return assign_node

    def read_stmt(self):
        read_node = Node("ERRORRRR", "READ")
        if(self.current_token() == "read"):
            self.match("read")
            if(str(self.token_type()) == "IDENTIFIER"):
                read_node.node_value = str(self.current_token())
                self.match(self.current_token())
            else: 
                read_node.is_errored = True
        else:
            read_node.is_errored = True
        return read_node

    def write_stmt(self):
        write_node = Node("ERRORRRR", "WRITE")
        if(self.current_token() == "write"):
            write_node.node_value = ""
            self.match("write")
            write_node.add_child(self.exp())
        else:
            write_node.is_errored = True
        return write_node

    def exp(self):
        temp = self.simple_exp()
        while self.current_token() in ["<", "="]:
            newtemp = self.comparison_op()
            if newtemp.is_errored:
                return temp  # return immediately if an error is encountered which means that the comparison_op() is errored so break the loop
            newtemp.add_child(temp)
            newtemp.add_child(self.simple_exp())
            temp = newtemp
        return temp

    def comparison_op(self):
        operator_node = Node("ERRORRRR", "OP")
        if self.current_token() in ["<", "="]:
            operator_node.node_value = str(self.current_token())
            self.match(self.current_token())
        else:
            operator_node.is_errored = True
        return operator_node

    def stmt_sequence(self):
        nodes = [self.statement()]
        if not nodes[-1].is_errored:
            if self.current_token() is not None:
                if self.current_token() != ";":
                    print("Missing ;")
                    error = Node("ERRORRRR", "ERROR")
                    # del nodes[-1]
                    error.is_errored = True
                    nodes.append(error)
            # else:
            while self.current_token() == ";":
                self.match(";")
                if ((self.current_token() == "if" or self.current_token() == "repeat" or self.current_token() == "read" or self.current_token() == "write") or self.token_type() == "IDENTIFIER"):
                    nodes.append(self.statement())
                else:
                    # if self.statement != None:
                    print("Error in Stmt Seq")
                    error = Node("ERRORRRR", "ERROR")
                    # del nodes[-1]
                    error.is_errored = True
                    nodes.append(error)
        if len(nodes) > 1:
            for i in range(len(nodes) - 1):
                nodes[i].sibling = nodes[i + 1]
        print("root nodes")
        for i in range(len(nodes)):
            print("node value: " + str(nodes[i].node_value) + " node type: " + str(nodes[i].node_type))
        print("end root nodes")
        print("nodes[0] value: " + str(nodes[0].node_value) + " nodes[0] type: " + str(nodes[0].node_type)+"\n")
        return nodes[0]

    def statement(self):
        #if self.current_token() == "end":
        #    return None
        if self.current_token() == "if":
            return self.if_stmt()
        elif self.current_token() == "repeat":
            return self.repeat_stmt()
        elif self.current_token() == "read":
            return self.read_stmt()
        elif self.current_token() == "write":
            return self.write_stmt()
        elif str(self.token_type()) == "IDENTIFIER":
            return self.assign_stmt()
        else:
            node = Node(None, "ERROR")
            node.is_errored = True
            return node

        #the error that makes me cryyyyyy
        #the error was that the token "end" is not handled
        # else:
        #     node = Node(None, "ERROR")
        #     node.is_errored = True
        #     return node

    def if_stmt(self):
        if_node = Node("ERRORRRR", "IF")
        if(self.current_token() == "if"):
            print("in if")
            self.match("if")
            condition = self.exp()
            if(self.current_token() == "then"):
                self.match("then")
                print("in then")
                if_node.node_value = "if"
                then_branch = self.stmt_sequence()
                if self.current_token() == "else":
                    self.match("else")
                    else_branch = self.stmt_sequence()
                    if self.current_token() == "end":
                        self.match("end")
                    else:
                        if_node.is_errored = True
                        return if_node
                    if_node.add_child(condition)
                    if_node.add_child(then_branch)
                    if else_branch:
                        if_node.add_child(else_branch)
                else:
                    if self.current_token() == "end":
                        self.match("end")
                        print("end matched *******")
                        if_node = Node("if", "IF")
                        if_node.add_child(condition)
                        if_node.add_child(then_branch)
                    else:
                        if_node.is_errored = True
                        print("**** end not matched *******")
                        if_node = Node("ERROR", "IF")
                        return if_node
                    # self.match("end")

                    return if_node

            else:
                print("in if error")
                if_node.is_errored = True
                return if_node
        else:
            print("in if error 2")
            if_node.is_errored = True
        return if_node

    def repeat_stmt(self):
        node = Node("ERRORRRR", "REPEAT")
        if self.current_token() == "repeat":
            print("1")
            self.match("repeat")
            body = self.stmt_sequence()
            if self.current_token() == "until":
                print("2")
                node.node_value = "repeat"
                self.match("until")
                condition = self.exp()
                node.add_child(body)
                node.add_child(condition)
                # if self.current_token() == ";":
                #     node.add_child(body)
                #     node.add_child(condition)
                # else:
                #     print("missing ; in until")
                #     node.is_errored = True
                #needs to check for ; after until
            else:
                print("3")
                node.is_errored = True
        else:
            print("4")
            node.is_errored = True
        return node

    def simple_exp(self):
        temp = self.term()
        while self.current_token() in ["+", "-"]:
            newtemp = self.addop()
            if newtemp.is_errored:
                return temp
            newtemp.add_child(temp)
            newtemp.add_child(self.term())
            temp = newtemp
        return temp

    def addop(self):
        operator_node = Node("ERRORRRR", "OP")
        if self.current_token() in ["+", "-"]:
            operator_node.node_value = str(self.current_token())
            self.match(self.current_token())
        else:
            operator_node.is_errored = True
        return operator_node

    def term(self):
        temp = self.factor()
        while self.current_token() in ["*", "/"]:
            newtemp = self.mulop()
            if newtemp.is_errored:
                return temp
            newtemp.add_child(temp)
            newtemp.add_child(self.factor())
            temp = newtemp
        return temp

    def mulop(self):
        operator_node = Node("ERRORRRR", "OP")
        if self.current_token() in ["*", "/"]:
            operator_node.node_value = str(self.current_token())
            self.match(self.current_token())
        else:
            operator_node.is_errored = True
        return operator_node

    def factor(self):
        if self.current_token() == "(":
            self.match("(")
            temp = self.exp()
            self.match(")")
            return temp
        elif str(self.token_type()) == "NUMBER":
            temp = Node(str(self.current_token()), "const", True)  # Terminal node
            self.match(self.current_token())
            return temp
        elif str(self.token_type()) == "IDENTIFIER":
            temp = Node(str(self.current_token()), "id", True)  # Terminal node
            self.match(self.current_token())
            return temp
        else:
            temp = Node("ERRORRRR", "ERROR")
            temp.is_errored = True
            return temp
    
    def parse(self):
        try :
            root = self.program()
            if root.is_errored:
                print("Error in program")
                return root
            '''
            The elif code block is checking if there are any tokens left in the input after 
            parsing the program. If there are, it means that the input contains some tokens
            that were not expected according to the grammar of the language, so it prints
            an error message and creates an errored node.
            '''
            # elif self.current_token() is not None:
            #     #print("Unexpected token: " + self.current_token())
            #     root = Node(None, "ERROR")
            #     root.is_errored = True

            print("root node value: " + str(root.node_value) + " root node type: " + str(root.node_type))
            return root
        except Exception as e:
            x = Node(None, "syntax error")
            x.is_errored =  True
            return x


   
