import Lex
from VMConstant import *

class Parser(object):
    _command_type = {'add':C_ARITHMETIC, 'sub':C_ARITHMETIC, 'neg':C_ARITHMETIC,
                     'eq' :C_ARITHMETIC, 'gt' :C_ARITHMETIC, 'lt' :C_ARITHMETIC,
                     'and':C_ARITHMETIC, 'or' :C_ARITHMETIC, 'not':C_ARITHMETIC,
                     'label':C_LABEL,    'goto':C_GOTO,      'if-goto':C_IF, 
                     'push':C_PUSH,      'pop':C_POP, 
                     'call':C_CALL,      'return':C_RETURN,  'function':C_FUNCTION}
                     
    _nullary = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not', 'return']
    _unary = ['label', 'goto', 'if-goto']
    _binary = ['push', 'pop', 'function', 'call']


    def __init__(self, filename):
        self.lex = Lex.Lex(filename)
        self._init_cmd_info()

    def _init_cmd_info(self):
        self._cmd_type = C_ERROR
        self._arg1 = ''
        self._arg2 = 0

    def hasMoreCommands(self):
        return self.lex.hasMoreCommands()

    def advance(self):
        self._init_cmd_info()

        self.lex.next_command()

        tok, val = self.lex.cur_token

        print(tok, val)

        if tok != Lex.ID:
            pass
        if val in self._nullary:
            self._nullary_command(val)
        elif val in self._unary:
            self._unary_command(val)
        elif val in self._binary:
            self._binary_command(val)


    def commandType(self) -> str:
        return self._cmd_type
            

    def arg1(self):
        return self._arg1

    def arg2(self):
        return self._arg2

    def _set_cmd_type(self, id):
        self._cmd_type = self._command_type[id]

    def _nullary_command(self, id):
        self._set_cmd_type(id)
        if self._command_type[id] == C_ARITHMETIC:
            self._arg1 = id
    
    def _unary_command(self, id):
        self._nullary_command(id)
        tok, val = self.lex.next_token()
        self._arg1 = val
    
    def _binary_command(self, id):
        self._unary_command(id)
        tok, val = self.lex.next_token()
        self._arg2 = int(val)