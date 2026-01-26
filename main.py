from lib8xp import to_8xp_binary, create_file_from_binary
from compiler import compile

program_name = "PYBASIC"
file_name = "py-basic"
program_code = compile("sample.py")
binary: str = to_8xp_binary(program_code,program_name)
print(binary)
create_file_from_binary(file_name,binary)