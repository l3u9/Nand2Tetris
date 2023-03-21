import Parser, Code, SymbolTable, sys


class Assembler(object):
    def __init__(self):
        self.symboltable = SymbolTable.SymbolTable()
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
                self.symboltable.addEntry(parser.symbol(), current_address)
        print(self.symboltable.symboltable)

    def pass2(self, file1, file2):
        parser = Parser.Parser(file1)
        print(self.symboltable.symboltable)
        code = Code.Code()
        f = open("output.hack", "w")
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
            if not self.symboltable.contains(symbol):
                self.symboltable.add_entry(symbol, self.symbol_addr)
                self.symbol_address += 1
            return self.symboltable.GetAddress(symbol)
        
asm = Assembler()

asm.pass1("Max.asm")
asm.pass2("Max.asm", "output.hack")
