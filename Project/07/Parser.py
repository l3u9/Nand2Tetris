

class Parser(object):
    C_PUSH = 0
    C_POP = 1
    C_LABEL = 2
    C_GOTO = 3
    C_IF = 4
    C_FUNCTION = 5
    C_RETURN = 6
    C_CALL = 7
    C_ARITHMETIC = 8
    def __init__(self, filename):
        f = open(filename, "r")
        self.data = f.read()
        self.codes = self.delete_comment(self.data.split("\n"))
        self.token = ""
        self.command = ""
        self.cmd_type = -1

        f.close()

    def delete_comment(self, codes):
        arr = []
        for i in codes:
            data = i
            if "//" in i:
                a = i.split("//")
                if a[0] == '':
                    continue
                else:
                    data = a[0].strip()
            if data == '':
                continue

            arr.append(data.strip())
        return arr

    def hasMoreCommands(self):
        if len(self.codes) == 0:
            return False
        else:
            return True

    def advance(self):
        self.get_command()


    def commandType(self) -> str:
        if self.command.startswith("push"):
            return self.C_PUSH
        elif self.command.startswith("pop"):
            return self.C_POP
        elif self.command.startswith("label"):
            return self.C_LABEL
        elif self.command.startswith("goto"):
            return self.C_GOTO
        elif self.command.startswith("if-goto"):
            return self.C_IF
        elif self.command.startswith("function"):
            return self.C_FUNCTION
        elif self.command.startswith("return"):
            return self.C_RETURN
        elif self.command.startswith("call"):
            return self.C_CALL
        else:
            return self.C_ARITHMETIC
            

    def arg1(self):
        if self.commandType() == self.C_ARITHMETIC:
            return self.command
        else:
            return self.command.split()[0]

    def arg2(self):
        if self.commandType() in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            return int(self.command.split()[2])
        else:
            raise ValueError("Invalid command type: {}".format(self.commandType()))


    def get_command(self):
        if self.hasMoreCommands():
            self.command = self.codes.pop(0)
            print(self.command)
        else:
            self.command = ""