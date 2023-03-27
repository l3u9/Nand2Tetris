from VMConstant import *
import os

class CodeWriter:
    def __init__(self, output_file_path: str):
        self.output_file = open(output_file_path, "w")
        self.current_function_name = None
        self.label_num = 0
        self._vm_file = ''

    def set_file_name(self, filename):
        self._vm_file, ext = os.path.splitext(filename)

    def write_init(self):
        self._a_command('256')
        self._c_command('D', 'A')
        self._comp_to_reg(R_SP, 'D')
        self.write_call('Sys.init', 0)

    def set_current_function_name(self, function_name: str) -> None:
        self.current_function_name = function_name

    def write_arithmetic(self, command_type: str) -> str:
        if   command_type == 'add':  self._binary('D+A')
        elif command_type == 'sub':  self._binary('A-D')
        elif command_type == 'neg':  self._unary('-D')
        elif command_type == 'eq':   self._compare('JEQ')
        elif command_type == 'gt':   self._compare('JGT')
        elif command_type == 'lt':   self._compare('JLT')
        elif command_type == 'and':  self._binary('D&A')
        elif command_type == 'or':   self._binary('D|A')
        elif command_type == 'not':  self._unary('!D')


    def write_push_pop(self, command_type: str, segment: str, index: int):
        if command_type == self.C_PUSH:
            self._push(segment, index)
        elif command_type == C_POP:
            self._pop(segment, index)

    def write_label(self, label: str):
        self.Instruction_l(label)

    def write_goto(self, label: str):
        self.Instruction_a(label)
        self.Instruction_c(None, '0', "JMP")

    def write_if(self, label: str):
        self._pop_to_dest("D")
        self.Instruction_a(label)
        self.Instruction_c(None, "D", "JNE")

    def write_call(self, function_name: str, num_args: int):
        return_address = self._new_label()
        self._push(S_CONST, return_address)
        self._push(S_REG, R_LCL)
        self._push(S_REG, R_ARG)
        self._push(S_REG, R_THIS)
        self._push(S_REG, R_THAT)
        self._load_sp_offset(-num_args-5)
        self._comp_to_reg(R_ARG, "D")
        self.Instruction_a(function_name)
        self.Instruction_c(None, "0", "JMP")
        self.Instruction_l(return_address)

    def write_return(self):
        self._reg_to_reg(R_FRAME, R_LCL)
        self.Instruction_a("5")
        self.Instruction_c("A", "D-A")
        self.Instruction_c("D", "M")
        self._comp_to_reg(R_RET, "D")
        self._pop(S_ARG, 0)
        self._reg_to_dest("D", R_ARG)
        self._comp_to_reg(R_SP, "D+1")
        self._prev_frame_to_reg(R_THAT)
        self._prev_frame_to_reg(R_THIS)
        self._prev_frame_to_reg(R_ARG)
        self._prev_frame_to_reg(R_LCL)
        self._reg_to_dest("A", R_RET)
        self.Instruction_c(None, "0", "JMP")

    def _prev_frame_to_reg(self, reg: str):
        self._reg_to_dest("D", R_FRAME)
        self.Instruction_c("D" "D-1")
        self._comp_to_reg(R_FRAME, "D")
        self.Instruction_c("A", "D")
        self.Instruction_c("D", "M")
        self._comp_to_reg(reg, "D")

    def write_function(self, function_name: str, num_locals: int):
        self.Instruction_l(function_name)
        for i in range(num_locals):
            self._push(S_CONST, 0)

    def _push(self, segment: str, index: int):
        if self._is_constant_seg(segment):
            self._val_to_stack(str(index))
        elif self._is_mem_seg(segment):
            self._mem_to_stack(self._asm_mem_seg(segment), index)
        elif self._is_reg_seg(segment):
            self._reg_to_stack(segment, index)
        elif self._is_static_seg(segment):
            self._static_to_stack(segment, index)
        self._inc_sp()

    def _pop(self, segment: str, index: int):
        self._dec_sp()
        if   self._is_mem_seg(segment):     
            self._stack_to_mem(self._asm_mem_seg(segment), index)
        elif self._is_reg_seg(segment):     
            self._stack_to_reg(segment, index)
        elif self._is_static_seg(segment):  
            self._stack_to_static(segment, index)

    def _pop_to_dest(self, dest: str):
        self._dec_sp()
        self._stack_to_dest(dest)

    def _is_mem_seg(self, segment: str):
        return segment in [S_LCL, S_ARG, S_THIS, S_THAT]

    def _is_reg_seg(self, segment: str):
        return segment in [S_REG, S_PTR, S_TEMP]

    def _is_static_seg(self, segment: str):
        return segment == S_STATIC

    def _is_constant_seg(self, segment: str):
        return segment == S_CONST

    def close(self) -> None:
        self.output_file.close()

    def _binary(self, comp:str) -> str:
        self._dec_sp()
        self._stack_to_dest("D")
        self._dec_sp()
        self._stack_to_dest("A")
        self.Instruction_c("D", comp)
        self._comp_to_stack('D')
        self._inc_sp()

    def _unary(self, comp:str) -> str:
        self._dec_sp()
        self._stack_to_dest("D")
        self._dec_sp()
        self._stack_to_dest("A")
        self.Instruction_c("D", comp)
        self._comp_to_stack("D")
        self._inc_sp()

    def _compare(self, jump: str):
        self._dec_sp()
        self._stack_to_dest("D")
        self._dec_sp()
        self._stack_to_dest("A")
        self.Instruction_c("D", "D-A")
        label_eq = self._jump("D", jump)
        self._comp_to_stack('0')
        label_ne = self._jump('0', 'JMP')
        self.Instruction_l(label_eq)
        self._comp_to_stack('-1')
        self.Instruction_l(label_ne)
        self._inc_sp()

    def _inc_sp(self) -> str:
        self.Instruction_a("SP")
        self.Instruction_c("M", "M+1")

    def _dec_sp(self) -> str:
        self.Instruction_a("SP")
        self.Instruction_c("M", "M-1")

    def _load_sp(self) -> str:
        self.Instruction_a("SP")
        self.Instruction_c("A", "M")

    def _val_to_stack(self, val: str):
        self.Instruction_a(val)
        self.Instruction_c("D", "A")
        self._comp_to_stack("D")

    def _reg_to_stack(self, segment: str, index: int):
        self._reg_to_dest('D', self._reg_num(segment, index))
        self._comp_to_stack('D')

    def _mem_to_stack(self, segment: str, index: int, indir: bool = True):
        self._load_seg(segment, index, indir)
        self.Instruction_c("D", "M")
        self._comp_to_stack("D")

    def _static_to_stack(self, index: int):
        self.Instruction_a(self._static_name(index))
        self.Instruction_c("D", "M")
        self._comp_to_stack("D")

    def _comp_to_stack(self, comp: str):
        self._load_sp()
        self.Instruction_c("M", comp)

    def _stack_to_reg(self, segment: str, index: int):
        self._stack_to_dest("D")
        self._comp_to_reg(self._reg_num(segment, index), "D")
    
    def _stack_to_mem(self, segment: str, index: int, indir: bool = True):
        self._load_seg(segment, index, indir)
        self._comp_to_reg(R_COPY, "D")
        self._stack_to_dest("D")
        self._reg_to_dest("A", R_COPY)
        self.Instruction_c("M", "D")

    def _stack_to_static(self, index: int):
        self._stack_to_dest("D")
        self.Instruction_a(self._static_name(index))
        self.Instruction_c("M", "D")

    def _stack_to_dest(self, dest: str):
        self._load_sp()
        self.Instruction_c(dest, "M")

    def _load_sp_offset(self, offset: int):
        self._load_seg(self._asm_reg(R_SP), offset)

    def _load_seg(self, segment: str, index: int, indir=True):
        if index == 0:
            self._load_seg_no_index(segment, indir)
        else:
            self._load_seg_index(segment, index, indir)

    def _load_seg_no_index(self, segment: str, indir: bool):
        self.Instruction_a(segment)
        if indir:
            self._indir("AD")

    def _load_seg_index(self, segment: str, index: int, indir: bool):
        comp = "D+A"
        if index < 0:
            index = -index
            comp = "A-D"
        self.Instruction_a(str(index))
        self.Instruction_c("D", "A")
        self.Instruction_a(segment)
        if indir:
            self._indir()
        
        self.Instruction_a(str(index))
        self.Instruction_c("D","A")
        self.Instruction_a(segment)
        if indir:
            self._indir()
        self.Instruction_c("AD", comp)


    def _reg_to_dest(self, dest: str, reg: int):
        self.Instruction_a(self._asm_reg(reg))
        self.Instruction_c(dest, "M")

    def _comp_to_reg(self, reg: int, comp: str):
        self.Instruction_a(self._asm_reg(reg))
        self.Instruction_c("M", comp)

    def _reg_to_reg(self, dest: str, src: str):
        self._reg_to_dest("D", src)
        self._comp_to_reg(dest, "D")

    def _indir(self, dest: str = 'A'):
        self.Instruction_c(dest, "M")

    def _reg_num(self, segment: str, index: int):
        return self._reg_base(segment) + index

    def _reg_base(self, segment: str):
        reg_base = {'reg' : R_R0, 'pointer' : R_PTR, 'temp' : R_TEMP}
        return reg_base[segment]

    def _static_name(self, index: int):
        return self._vm_file + '.' + str(index)

    def _asm_mem_seg(self, segment: str):
        asm_label = {S_LCL:'LCL', S_ARG:'ARG', S_THIS:'THIS', S_THAT:'THAT'}
        return asm_label[segment]

    def _asm_reg(self, regnum: int):
        return "R " + str(regnum)

    def _jump(self, comp: str, jump: str):
        label = self._new_label()
        self.Instruction_a(label)
        self.Instruction_c(None, comp, label)
        return label
    
    def _new_label(self):
        self.label_num += 1
        return 'LABEL ' + str(self.label_num)

    def Instruction_a(self, address: str):
        self.output_file.write("@" + address + "\n")
    
    def Instruction_c(self, dest: str, comp: str, jump :str == None):
        if dest != '':
            self.output_file.write(dest + "=")
        self.output_file.write(comp)

        if jump != '':
            self.output_file.write(';' + jump)
        self.output_file.write("\n")

    def Instruction_l(self, label: str):
        self.output_file.write("(" + label + ")" + "\n")