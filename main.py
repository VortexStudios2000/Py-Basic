from lib8xp import to_8xp_binary, create_file_from_binary
from compiler import compile

program_name = "SERENITY"
file_name = "serenity"
#program_code:str = "E1 3F E0 35 2B 31 33 2B 2A 53 54 41 52 54 49 4E 47 29 53 45 52 45 4E 49 54 59 2A"
program_code = compile("sample.py")
binary: str = to_8xp_binary(program_code,program_name)
print(binary)
create_file_from_binary(file_name,binary)