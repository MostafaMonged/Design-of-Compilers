code = """{ Sample program in TINY language –
computes factorial}
read x; {input an integer }
if 0 < x then { don’t compute if 
x <= 0 }
fact := 1;
repeat 
fact := fact * x;
x := x - 1
until x = 0;
write fact { output factorial of x 
}
end"""

code_sum = """{ Sample program in TINY language – computes sum of x and y}
read x; {input an integer }
read y; {input an integer }
sum := x + y;
write sum; { output sum of x and y }"""


class Scanner:
    def __init__(self):
        self.code = ""
        self.i = 1
        self.Reserved_Words = [
            "if",
            "then",
            "else",
            "end",
            "repeat",
            "until",
            "read",
            "write",
        ]
        self.Special_Symbols = [
            "+",
            "-",
            "*",
            "/",
            "=",
            "<",
            "(",
            ")",
            ";",
            ":=",
            "{",
            "}",
        ]
        self.inside_comment = False
        self.finish = False

    def another_code(self, tiny_code):
        self.code = tiny_code
        self.i = 1
        self.inside_comment = False
        self.finish = False

    def get_next_token(self):
        if self.i > len(self.code):
            self.finish = True
            return
        j = self.i
        if (self.code[self.i - 1] in self.Special_Symbols) or self.code[
            self.i - 1
        ] == ":":
            if self.code[self.i - 1] == ":" and self.code[self.i] == "=":
                self.i += 2
                return [":=", "Special_Symbol"]
            else:
                if self.code[self.i - 1] == "{":
                    self.inside_comment = True
                if self.code[self.i - 1] == "}":
                    self.inside_comment = False
                self.i += 1
                return [self.code[self.i - 2], "Special_Symbol"]
        elif self.code[self.i - 1] == " ":
            self.i += 1
            return self.get_next_token()
        elif self.code[self.i - 1] == "\n":
            self.i += 1
            return self.get_next_token()
        elif self.code[self.i - 1].isdigit():
            temp3 = self.code[self.i - 1]
            self.i += 1
            while True:
                if self.i <= len(self.code):
                    if self.code[self.i - 1].isdigit():
                        temp3 += self.code[self.i - 1]
                        self.i += 1
                    else:
                        break
                else:
                    break
            return [temp3, "number"]
        else:
            temp = ""
            temp2 = ""
            if self.code[self.i - 1].isalpha():
                if self.inside_comment:
                    # print(self.inside_comment)
                    while True:
                        if self.code[j - 1] != "}":
                            temp2 += str(self.code[j - 1])
                            j += 1
                        else:
                            self.inside_comment = False
                            self.i = j
                            return self.get_next_token()
                else:
                    while True:
                        if self.code[j - 1].isalpha() and j < len(self.code):
                            # print("self.code[j-1].isalpha(): "+str(self.code[j-1].isalpha()))
                            temp += str(self.code[j - 1])
                            j += 1
                            if j == len(self.code) and self.code[j - 1].isalpha():
                                temp += str(self.code[j - 1])
                                self.finish = True
                        else:
                            # print(temp)
                            if temp in self.Reserved_Words:
                                self.i = j
                                return [temp, "Reserved_Word"]
                            else:
                                self.i = j
                                return [temp, "Identifier"]

    def scan(self):
        gui_show_list = []
        while not self.finish:
            next_token = self.get_next_token()
            if next_token is not None:
                gui_show_tuple = (str(next_token[0]), str(next_token[1]))
                gui_show_list.append(gui_show_tuple)
        return gui_show_list


# if __name__ == "__main__":
#     sc = Scanner(code)
#     print(sc.scan())
#     print()
#     sc.another_code(code_sum)
#     print(sc.scan())

    # while not sc.finish:
    #     print(sc.get_next_token())
    # print("*************another_code***********")
    # sc.another_code(code_sum)
    # while not sc.finish:
    #     print(sc.get_next_token())
