import re


A_COMMAND = 1
C_COMMAND = 2
L_COMMAND = 3

class Parser(object):
    def __init__(self, filename):
        self.target_file = open(filename, "r")
        self.data = self.target_file.read()
        self.codes = self.data.split("\n")

    
    def hasMoreCommands(self):
        if len(self.codes) == 0:
            return False
        else:
            return True

    def advance(self):
        pass

    def command_type(self, code):
        if code.startswith("@"):
            return A_COMMAND
        
        pass

    def symbol(self):
        pass

    def dest(self):
        pass

    def comp(self):
        pass

    def jump(self):
        pass
    
