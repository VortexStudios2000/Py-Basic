blacklist: list[str] = ["from libTIcompatibility import *\n","\n","# __start__ #\n"]

ASCII_chars: list[str] =    [",",'"'," ",".","+","-","*","/","=",")"]
TI_chars: list[str] =       ["+","*",")",":","p","q","‚","ƒ","j","~"]

names:list[str] =     ["ClrHome()","Output(","+",")","*",":","Wait(","Disp(","p","q","‚","ƒ","j","Input(","Sqrt(","^2","~","`"]
commands:list[str] =  ["E1","E0","2B","29","2A","3A","EF96","DE","70","71","82","83","6A","DC","BC","0D","11","04"]

#sqrt A  ^2 +  B  ^2 )  -> C
#BC   41 0D 70 42 0D 11 04 43

def to_hex_2byte_multiple(value:str|int|bytes|bytearray) -> str:
    if isinstance(value, int):
        hex_str = f"{value:X}"
    elif isinstance(value, str):
        hex_str:str = ""
        for char in value:
            if char in names:
                hex_str += lookup_function(char)
            else:
                hex_str += char.encode().hex().upper()
    elif isinstance(value, (bytes, bytearray)):
        hex_str = value.hex().upper()
    else:
        raise TypeError("Unsupported type")

    pad = (-len(hex_str)) % 2
    return "0" * pad + hex_str

def lookup_function(name:str) -> str:
    idx = names.index(name)
    return commands[idx]

def split_command(item:str):
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
    return command,next_item

def reformat(item:str) -> str:
    result = item.strip("\n")
    if result[0] in "abcdefghijklmnopqrstuvwxyz" and result[1] == "=":
        var = result[0].upper()
        if result[2:8] == "Input(":
            result = result[2:len(result)-1] + "," + var + ")"
        else:
            result = result[2:len(result)-1] + "`" + var + ")"
    return result

def parse_file(lines:list[str]):
    usable_data:list[str] = []
    can_start = False
    for item in lines:
        if item == "# __start__ #\n":
            can_start = True
        if not can_start:
            continue
        if not item in blacklist:
            usable_data.append(reformat(item))

    compiled:str = ""
    for item in usable_data:
        if item in names:
            compiled += lookup_function(item)
        else:
            # get main command
            command,next_item = split_command(item)
            compiled += lookup_function(command)

            # replace characters with TI-compatible ones
            replace_list:list[str] = list(next_item[0:len(next_item)-1])
            for i in range(len(replace_list)):
                char: str = replace_list[i]
                if char in ASCII_chars:
                    replace_list[i] = TI_chars[ASCII_chars.index(char)]
                else:
                    replace_list[i] = replace_list[i].upper()
                
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
                elif arguments[i][-1] =="~":
                    subcmd, rest = split_command(arguments[i])
                    new_arguments.append(subcmd)
                    new_arguments.append(rest[0:len(rest)-1])
                    new_arguments.append("~")
                else:
                    new_arguments.append(arguments[i])
            arguments = new_arguments
            #print(arguments)

            for arg in arguments:
                if arg in names:
                    compiled += lookup_function(arg)
                    #print(bytes.fromhex(lookup_function(arg)))
                else:
                    compiled += to_hex_2byte_multiple(arg)
                    #print(bytes.fromhex(to_hex_2byte_multiple(arg)))

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
    