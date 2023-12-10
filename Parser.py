class Parser:
    def __init__(self, scanner_output):
        self.tokens_list = scanner_output
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
        # program()
        pass
