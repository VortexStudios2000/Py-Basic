blacklist: list[str] = ["from libTIcompatibility import *\n","\n"]

names:list[str] =     ["ClrHome()","Output(","+",")","*",":","Wait("]
commands:list[str] =  ["E1","E0","2B","29","2A","3A","EF96"]

def to_hex_2byte_multiple(value:str|int|bytes|bytearray) -> str:
    if isinstance(value, int):
        hex_str = f"{value:X}"
    elif isinstance(value, str):
        hex_str = value.encode().hex().upper()
    elif isinstance(value, (bytes, bytearray)):
        hex_str = value.hex().upper()
    else:
        raise TypeError("Unsupported type")

    pad = (-len(hex_str)) % 2
    return "0" * pad + hex_str

def lookup_function(name:str) -> str:
    idx = names.index(name)
    return commands[idx]

def is_complex(name:str) -> bool:
    if name in names: return False
    else: return True

def parse_file(lines:list[str]):
    usable_data:list[str] = []
    for item in lines:
        if not item in blacklist:
            usable_data.append(item.strip("\n"))
    
    compiled:str = ""
    for item in usable_data:
        if not is_complex(item):
            compiled += lookup_function(item)
        else:
            # get main command
            current_item: str = item
            next_item:str = ""
            command:str = ""
            passed = False
            for char in current_item:
                if not passed:
                    command += char
                else:
                    next_item += char
                if char == "(":
                    passed = True
            
            # replace characters with TI-compatible ones
            replace_list:list[str] = list(next_item[0:len(next_item)-1])
            for i in range(len(replace_list)):
                char: str = replace_list[i]
                if char == ",": replace_list[i] = "+"
                if char == '"': replace_list[i] = "*"
                if char == " ": replace_list[i] = ")"
                if char == ".": replace_list[i] = ":"
            current_item = ""
            for item in replace_list:
                current_item += item

            new_arguments:list[str] = []
            # split arguments
            # TODO: make sure commas quotation marks dont get split as seperate arguments
            arguments: list[str] = current_item.split("+")
            new_arguments.append(arguments[0])
            for i in range(1,len(arguments)):
                new_arguments.append("+")
                new_arguments.append(arguments[i])
            arguments = new_arguments

            # seperate quotes
            new_arguments = []
            for i in range(len(arguments)):
                if arguments[i][0] == "*" and arguments[i][len(arguments[i])-1] == "*":
                    new_arguments.append("*")
                    new_arguments.append(arguments[i][1:len(arguments[i])-1])
                    new_arguments.append("*")
                else:
                    new_arguments.append(arguments[i])
            arguments = new_arguments

            compiled += lookup_function(command)
            for arg in arguments:
                if is_complex(arg):
                    compiled += to_hex_2byte_multiple(arg)
                else:
                    compiled += lookup_function(arg)

        compiled += "3F"
    compiled = compiled[0:len(compiled)-2]

    return compiled

def compile(filename:str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines_list: list[str] = f.readlines()
            return parse_file(lines_list)
    except FileNotFoundError:
        print(f"Error: The file '{target_name}' was not found.")
        return "ERROR"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "ERROR"

if __name__ == "__main__":
    # sample run
    target_name = "sample.py"
    print(compile(target_name))
    