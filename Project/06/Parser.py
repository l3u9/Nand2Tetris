import re
import SymbolTable

class Parser(object):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3
    symboltable = SymbolTable.SymbolTable()
    def __init__(self, filename):
        f = open(filename, "r")
        self.data = f.read()
        self.codes = self.delete_comment(self.data.split("\n"))
        self.token = ""
        self.command = ""
        self.cmd_type = -1
        self.symbol_token = ""
        self.dest_token = ""
        self.comp_token = ""
        self.jump_token = ""
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
        if re.findall(r'@[a-zA-Z0-9_]+', self.command):
            self.process_a_command(self.command)
            self.token = self.symbol()

        elif re.findall(r'\([a-zA-Z_]+\)', self.command):
            self.process_l_command(self.command)
            self.token = self.symbol()
        elif "=" in self.command or ";" in self.command:
            self.process_c_command()

    def command_type(self):
        return self.cmd_type
    
    def symbol(self):
        return self.symbol_token

    def dest(self):
        return self.dest_token

    def comp(self):
        return self.comp_token

    def jump(self):
        return self.jump_token

    def process_a_command(self, code):
        self.cmd_type = self.A_COMMAND
        data = re.findall(r"[a-zA-Z0-9]", code)
        self.symbol_token = "".join(data)

    def process_l_command(self, code):
        self.cmd_type = self.L_COMMAND
        data = re.findall(r"[a-zA-Z0-9]", code)
        self.symbol_token = "".join(data)

    def process_c_command(self):
        self.cmd_type = self.C_COMMAND
        if ";" in self.command:
            data = self.command.split(";")
            self.comp_token = data[0]
            self.jump_token = data[-1]
            self.dest_token = self.symboltable.GetAddress(self.token)
        elif "=" in self.command:
            data = self.command.split("=")
            self.comp_token = data[-1]
            self.jump_token = ""
            self.dest_token = data[0]

    def get_command(self):
        self.command = self.codes.pop(0)    
    
