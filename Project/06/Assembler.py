import Parser, Code, SymbolTable, sys


class Assembler(object):
    def __init__(self):
        self.symbols = SymbolTable.SymbolTable()
        self.symbol_address = 16 #initial register symbol table size 15

    def pass1(self, file):
        parser = Parser.Parser(file)
        current_address = 0
        while parser.hasMoreCommands():
            parser.advance()
            type = parser.command_type()
            if type == parser.A_COMMAND or type == parser.C_COMMAND:
                current_address += 1
            elif type == parser.L_COMMAND:
                self.symbols.addEntry(parser.symbol(), current_address)

    def pass2(self, file1, file2):
        parser = Parser.Parser(file1)
        code = Code.Code()
        f = open(file2, "w")
        while parser.hasMoreCommands():
            parser.advance()
            type = parser.command_type()
            if type == parser.A_COMMAND:
                f.write( code.gen_a_instruction(self.get_address(parser.symbol())) + '\n' )
            elif type == parser.C_COMMAND:
                f.write( code.gen_c_instruction(parser.dest(), parser.comp(), parser.jump()) + '\n' )
            elif type == parser.L_COMMAND:
                pass
        
        f.close()
    
    def get_address(self, symbol):
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbols.contains(symbol):
                self.symbols.addEntry(symbol, self.symbol_address)
                self.symbol_address += 1
            return self.symbols.GetAddress(symbol)
        
asm = Assembler()

filename = sys.argv[1]

if "asm" in filename:
    file1 = filename
    name = filename.split(".")[0]
    file2 = name + ".hack"

asm.pass1(file1)
asm.pass2(file1, file2)
