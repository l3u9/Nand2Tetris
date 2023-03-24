from Parser import Parser
from CodeWriter import CodeWriter

def translate_vm_file(vm_file_path):
    # output file name
    asm_file_name = vm_file_path[:-3] + ".asm"
    
    # Initialize Parser and CodeWriter
    parser = Parser(vm_file_path)
    code_writer = CodeWriter(asm_file_name)
    
    # Loop through each command in the input file
    while parser.hasMoreCommands():
        parser.advance()
        command_type = parser.commandType()
        
        # Write the command to assembly code
        if command_type == "C_ARITHMETIC":
            code_writer.writeArithmetic(parser.arg1())
        elif command_type in ["C_PUSH", "C_POP"]:
            code_writer.writePushPop(command_type, parser.arg1(), parser.arg2())

    # Close the output file
    code_writer.close()

translate_vm_file("BasicTest.vm")