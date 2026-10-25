from lib8xp import to_8xp_binary, create_file_from_binary
from pybasic import compile

program_name = "PYBASIC"
output_file_name = "PY-BASIC-2"
python_program_name = "sample.py"

program_code = compile(f"programs/{python_program_name}")
binary: str = to_8xp_binary(program_code,program_name)
print(binary)
create_file_from_binary(f"builds/{output_file_name}",binary)