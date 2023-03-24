class CodeWriter:
    def __init__(self, output_file_path: str):
        self.output_file = open(output_file_path, "w")
        self.current_function_name = None
        self.label_num = 0
        self.call_num = 0

    def set_current_function_name(self, function_name: str) -> None:
        self.current_function_name = function_name

    def write_arithmetic(self, command: str) -> str:
        pass

    def write_push_pop(self, command_type: str, segment: str, index: int) -> str:
        pass

    def write_label(self, label: str) -> str:
        pass

    def write_goto(self, label: str) -> str:
        pass

    def write_if(self, label: str) -> str:
        pass

    def write_call(self, function_name: str, num_args: int) -> str:
        pass

    def write_return(self) -> str:
        pass

    def write_function(self, function_name: str, num_locals: int) -> str:
        pass

    def close(self) -> None:
        self.output_file.close()