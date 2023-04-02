from JackConst import *
from JackTokenizer import JackTokenizer

OP_LIST = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

class CompilationEngine():
    def __init__(self, inputfile, outputfile):
        self.output_file = open(outputfile, "w+")
        self.tokenizer = JackTokenizer(inputfile)


    def write(self, string):
        self.output_file.write(string)

    def CompileClass(self):
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            self.write("<class>\n")

            self.write(self.tokenizer.toXML())

            self.tokenizer.advance()
            self.write(self.tokenizer.toXML())

            self.tokenizer.advance()
            self.write(self.tokenizer.toXML())

            self.tokenizer.advance()
            while self.tokenizer.keyword() == "static" or \
                    self.tokenizer.keyword() == "field":
                self.CompileClassVarDec()
            while self.tokenizer.keyword() == "constructor" or \
                    self.tokenizer.keyword() == "function" \
                    or self.tokenizer.keyword() == "method":
                self.CompileSubroutine()

            self.write(self.tokenizer.toXML())

            self.write("</class>\n")
            


    def CompileClassVarDec(self):
        self.write('<classVarDec>')

        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.compile_varname()


        self.write('</classVarDec>')


    def CompileSubroutine(self):
        self.write("<subroutineDec>\n")
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        if self.tokenizer.tokenType() == T_KEYWORD:
            self.write(self.tokenizer.toXML())
        elif self.tokenizer.tokenType() == T_ID:
            self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.compileParameterList()

        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        # compile subroutineBody:
        self.write("<subroutineBody>\n")
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        while self.tokenizer.keyword() == "var":
            self.compileVarDec()

        self.compileStatements()

        self.write(self.tokenizer.toXML())
        self.write("</subroutineBody>\n")
        self.write( "</subroutineDec>\n")
        self.tokenizer.advance()


    def compileParameterList(self):
        self.write("<parameterList>\n")
        # self.write(self.tokenizer.toXML())
        while self.tokenizer.tokenType() != T_SYM:
            if self.tokenizer.tokenType() == T_KEYWORD:
                self.write(self.tokenizer.toXML())
            elif self.tokenizer.tokenType() == T_ID:
                self.write(self.tokenizer.toXML())
            self.tokenizer.advance()
            self.write(self.tokenizer.toXML())
            self.tokenizer.advance()
            if self.tokenizer.symbol() == ",":
                self.write(self.tokenizer.toXML())
                self.tokenizer.advance()

        self.write("</parameterList>\n")

    def compileVarDec(self):
        self.write("<varDec>\n")

        self.write(self.tokenizer.toXML())
        self.tokenizer.advance()
        self.compile_varname()

        self.write("</varDec>\n")

    def compileStatements(self):
        self.write("<statements>\n")
        while self.tokenizer.tokenType() == T_KEYWORD:
            if self.tokenizer.keyword() == KW_LET:
                self.compileLet()
            elif self.tokenizer.keyword() == KW_IF:
                self.compileIf()
            elif self.tokenizer.keyword() == KW_WHILE:
                self.compileWhile()
            elif self.tokenizer.keyword() == KW_DO:
                self.compileDo()
            elif self.tokenizer.keyword() == KW_RETURN:
                self.compileReturn()
        
        # self.write(self.tokenizer.toXML())
        # self.tokenizer.advance()
    
        self.write("</statements>\n")

    def compileDo(self):
        self.write("<doStatement>\n")
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()

        self.write(self.tokenizer.toXML())
        self.tokenizer.advance()
        if self.tokenizer.symbol() == ".":
            self.write(self.tokenizer.toXML())
            self.tokenizer.advance()
            self.write(self.tokenizer.toXML())
            self.tokenizer.advance()

        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.CompileExpressionList()

        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.write(self.tokenizer.toXML())

        self.write("</doStatement>\n")

        self.tokenizer.advance()

    def compileLet(self):
        self.write("<letStatement>\n")
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        if self.tokenizer.symbol() == "[":
            self.write(self.tokenizer.toXML())
            self.tokenizer.advance()
            self.CompileExpression()
            self.write(self.tokenizer.toXML())
            self.tokenizer.advance()
        
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.CompileExpression()
        self.write(self.tokenizer.toXML())

        self.write("</letStatement>\n")
        self.tokenizer.advance()

    def compileWhile(self):
        self.write("<whileStatement>\n")
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.CompileExpression()

        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.compileStatements()

        self.write(self.tokenizer.toXML())

        self.write("</whileStatement>\n")
        self.tokenizer.advance()
    
        

    def compileReturn(self):
        self.write("<returnStatement>\n")
        self.write(self.tokenizer.toXML())
        
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != T_SYM and self.tokenizer.symbol() != ";":
            self.CompileExpression()
        self.write(self.tokenizer.toXML())

        self.write("</returnStatement>\n")
        self.tokenizer.advance()



    def compileIf(self):
        self.write("<ifStatement>\n")
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.CompileExpression()

        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.write(self.tokenizer.toXML())

        self.tokenizer.advance()
        self.compileStatements()

        self.write(self.tokenizer.toXML())
        
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == T_KEYWORD and self.tokenizer.keyword() == "else":
            self.write(self.tokenizer.toXML())
        
            self.tokenizer.advance()
            self.write(self.tokenizer.toXML())

            self.tokenizer.advance()
            self.compileStatements()

            self.write(self.tokenizer.toXML())
            self.tokenizer.advance()
        
        self.write("</ifStatement>\n")




    def CompileExpression(self):
        self.write("<expression>\n")

        self.CompileTerm()
        while self.tokenizer.tokenType() == T_SYM and self.tokenizer.symbol() in OP_LIST:
            self.write(self.tokenizer.toXML())
            self.tokenizer.advance()
            self.CompileTerm()
        
        self.write("</expression>\n")
    
    def CompileTerm(self):
        sanity_check = True
        self.write("<term>\n")
        if self.tokenizer.tokenType() == T_NUM:
            self.write(self.tokenizer.toXML())
        elif self.tokenizer.tokenType() == T_STR:
            self.write(self.tokenizer.toXML())
        elif self.tokenizer.tokenType() == T_KEYWORD:
            self.write(self.tokenizer.toXML())
        elif self.tokenizer.tokenType() == T_ID:
            self.write(self.tokenizer.toXML())


            self.tokenizer.advance()
            sanity_check = False
            if self.tokenizer.symbol() == "[":
                sanity_check = True
                self.write(self.tokenizer.toXML())
                self.tokenizer.advance()
                self.CompileExpression()
                self.write(self.tokenizer.toXML())
            elif self.tokenizer.symbol() == ".":
                sanity_check = True
                self.write(self.tokenizer.toXML())
                self.tokenizer.advance()
                self.write(self.tokenizer.toXML())
                self.tokenizer.advance()
                self.write(self.tokenizer.toXML())
                self.tokenizer.advance()
                self.CompileExpressionList()
                self.write(self.tokenizer.toXML())
            elif self.tokenizer.symbol() == "(":
                sanity_check = True
                self.write(self.tokenizer.toXML())
                self.tokenizer.advance()
                self.CompileExpressionList()
                self.write(self.tokenizer.toXML())

        elif self.tokenizer.symbol() == "(":
            self.write(self.tokenizer.toXML())
            self.tokenizer.advance()
            self.CompileExpression()
            self.write(self.tokenizer.toXML())
        elif self.tokenizer.symbol() == "~" or self.tokenizer.symbol() == \
                "-":
            self.write(self.tokenizer.toXML())
            self.tokenizer.advance()
            self.CompileTerm()
            sanity_check = False

        if sanity_check:
            self.tokenizer.advance()

        self.write("</term>\n")

            
    def CompileExpressionList(self):
        self.write("<expressionList>\n")

        if self.tokenizer.tokenType() != T_SYM and self.tokenizer.symbol() != ")":
            self.CompileExpression()
            while self.tokenizer.tokenType() == T_SYM and self.tokenizer.symbol() == ",":
                self.write(self.tokenizer.toXML())
                self.tokenizer.advance()
                self.CompileExpression()
        if self.tokenizer.symbol() =="(":
            self.CompileExpression()
            while self.tokenizer.tokenType() == T_SYM and self.tokenizer.symbol() == ",":
                self.write(self.tokenizer.toXML())
                self.tokenizer.advance()
                self.CompileExpression()

        self.write("</expressionList>\n")


    def compile_varname(self):
        if self.tokenizer.tokenType() == T_KEYWORD:
            self.write(self.tokenizer.toXML())
        elif self.tokenizer.tokenType() == T_ID:
            self.write(self.tokenizer.toXML())
        
        self.tokenizer.advance()
        self.write(self.tokenizer.toXML())
        self.tokenizer.advance()

        while self.tokenizer.symbol() == ",":
            self.write(self.tokenizer.toXML())
            self.tokenizer.advance()
            self.write(self.tokenizer.toXML())
            self.tokenizer.advance()
        self.write(self.tokenizer.toXML())
        self.tokenizer.advance()


