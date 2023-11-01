
# character = '.'
# if character.isalpha():
#     print("The character is alphabetical.")
# else:
#     print("The character is not alphabetical.")
#elif (code[self.i] not in Special_Symbols) and code[self.i] != ":" and code[self.i] == " ":
#print("else" in Reserved_Words)
# character = '5'
# if character.isdigit():
#     print("The character is a numeric digit.")
# else:
#     print("The character is not a numeric digit.")

code ='''{ Sample program in TINY language –
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
end
'''


class Scanner():
    def __init__(self, code):
        self.code = code
        self.i=1
        self.Reserved_Words = ["if", "then", "else", "end", "repeat", "until", "read", "write"]
        self.Special_Symbols = ["+", "-", "*", "/", "=", "<", "(", ")", ";", ":=", "{", "}"]
        self.inside_comment = False
        self.finish=False

    def get_next_token(self):
        if self.i >= len(code) :
            self.finish=True
            return
        j = self.i
        if (code[self.i-1] in self.Special_Symbols) or code[self.i-1] == ":":
            if code[self.i-1] == ":" and code[self.i] == "=":
                self.i += 2
                return [":=", "Special_Symbol"]
            else:
                if code[self.i-1]=="{" :
                    self.inside_comment = True
                if code[self.i - 1] == "}":
                    self.inside_comment = False
                self.i += 1
                return [code[self.i-2],"Special_Symbol"]
        elif code[self.i-1] == " ":
            self.i += 1
            j = self.i
            return self.get_next_token()
        elif code[self.i-1] == "\n" :
            self.i += 1
            return self.get_next_token()
        elif code[self.i-1].isdigit() :
            temp3=code[self.i-1]
            self.i += 1
            while True:
                if code[self.i-1].isdigit():
                    temp3 += code[self.i - 1]
                    self.i += 1
                else:
                    break
            return [temp3,"number"]
        else:
            temp = ""
            temp2=""
            if self.code[self.i - 1].isalpha():
                if self.inside_comment:
                    #print(self.inside_comment)
                    while True:
                        if self.code[j - 1] != "}":
                            temp2 += str(self.code[j - 1])
                            j += 1
                        else:
                            self.inside_comment = False
                            self.i = j
                            return self.get_next_token()
                while True:
                    if self.code[j-1].isalpha():
                        #print("self.code[j-1].isalpha(): "+str(self.code[j-1].isalpha()))
                        temp += str(self.code[j-1])
                        j += 1
                    else:
                        #print(temp)
                        if temp in self.Reserved_Words:
                            self.i = j
                            return [temp, "Reserved_Word"]
                        else:
                            self.i = j
                            return [temp, "Identifier"]

sc = Scanner(code)

for k in range(40):
    print(sc.get_next_token())
    #print(" iteration number:"+str(k))
