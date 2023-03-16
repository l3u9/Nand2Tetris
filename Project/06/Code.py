class Code(object):
    def __init__(self):
        self.dest_code = ["", "M", "D", "MD", "A", "AM", "AD", "AMD"]
        self.jump_code = ["", "JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]
        self.comp_code = {
            '0':'0101010',  '1':'0111111',  '-1':'0111010', 'D':'0001100', 
            'A':'0110000',  '!D':'0001101', '!A':'0110001', '-D':'0001111', 
            '-A':'0110011', 'D+1':'0011111','A+1':'0110111','D-1':'0001110', 
            'A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111', 
            'D&A':'0000000','D|A':'0010101',
            'M':'1110000', '!M':'1110001', '-M':'1110011', 'M+1':'1110111',
            'M-1':'1110010', 'D+M':'1000010', 'D-M':'1010011', 'M-D':'1000111',
            'D&M':'1000000', 'D|M':'1010101'
        }

    def gen_a_instruction(self, address):
        return self.int_to_bin(address).zfill(16)
    
    def gen_c_instruction(self, dest, comp, jump):
        return '111' + self.comp(comp) + self.dest(dest) + self.jump(jump)

    def dest(self, code):
        return self.int_to_bin(self.dest_code.index(code)).zfill(3)

    def comp(self, code):
        return self.comp_code[code]

    def jump(self, code):
        return self.int_to_bin(self.jump_code.index(code)).zfill(3)

    def int_to_bin(self, i):
        return bin(i)[2:]
    
