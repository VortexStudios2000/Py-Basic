# ANSI escape codes for colors in terminal
RESET = "\x1b[0m"
RED = "\x1b[31m"
YELLOW = "\x1b[33m"
GREEN = "\x1b[32m"

# Direct substitutions for the TI-84 Calculator
commands = ["linebreak","ClrHome","Wait","Output(","Input","Disp","√(","Lbl","Goto","Menu(","Pause","Stop","DelVar"]
hex_commands = ["3F","E1","EF 96","E0","DC","DE","BC","D6","D7","E6","D8","D9","BB54"]
chars =     [",",'"'," ",".",":","-","+","*","/","=","(",")","→","²","^","Π","_"]
hex_chars = ["2B","2A","29","3A","3E","71","70","82","83","6A","10","11","04","0D","F0","AC","BBD9"]

# Currently-supported
line_forms: list[str] = ["{/varname}{/space}{=}{/space}{Input(}{/string}",
                         "{/varname}{/space}{=}{/space}{int(input(}{/string}",
                         "{/varname}{/space}{=}{/space}{float(input(}{/string}",
                         "{/varname}{/space}{=}{/space}{/value}",
                         "{ClrHome()}",
                         "{Wait}{/value}",
                         "{Disp(}{/value}",
                         "{Output(}{/value}",
                         "{print(}{/value}",
                         "{/label}{()}",
                         "{def}{/space}{/label}{():}",
                         "{Pause}{/value}",
                         "{Stop()}",
                         "{Menu(}{/value}"]

def to_hex_2byte_multiple(value:int|str) -> str:
    # for standard conversion to hex
    if isinstance(value, int):
        hex_str = f"{value:X}"
    elif isinstance(value, str): #type:ignore
        hex_str:str = ""
        for char in value:
            hex_str += char.encode().hex().upper()
    else:
        raise TypeError("Unsupported type")

    pad = (-len(hex_str)) % 2
    return "0" * pad + hex_str

def read_program(name:str,filter:bool=True) -> list[str]:
    # filters out unecessary header code for python file
    program:list[str] = []
    try: # read file
        with open(name, 'r', encoding='utf-8') as f:
            lines_list: list[str] = f.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{target_name}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    if filter:
        # get init section
        started = False
        for line in lines_list:
            if not started and line == "# __init__ #\n":
                started = True
                continue
            if started and line[0] != "#" and line.strip() != "":
                program.append(line.strip())

        # get actual code
        started = False
        for line in lines_list:
            if not started and line == "# __start__ #\n":
                started = True
                continue
            if  started and line == "# __init__ #\n":
                break
            if started and line[0] != "#" and line.strip() != "":
                program.append(line.strip())
    else:
        for item in lines_list:
            program.append(item.strip())
    
    program.insert(0,name)
    return program

def python_to_basic(program:list[str]) -> list[str]:
    # reformat python into TI-Basic
    # after this stage, almost all code should be copy-pasteable into TI-Connect CE program editor
    basic:list[str] = []
    error = False

    # parses the complex menu function of varying number of parameters
    def parse_menu_func(data:str) -> str:
        line = data[0:-2]
        itemList = line.replace("[","").replace("]","").split(",")
        final = "Menu(" + itemList.pop(0) + ","

        numPairs = int(len(itemList)/2)
        for i in range(numPairs):
            final += itemList[i] + "," + itemList[i+numPairs] + ","
        
        final = final[0:-1]
        return final

    for line in program[1:-1]:

        output = match_many_forms(line_forms,line)
        success = output[0]
        line_type = output[1]
        params = output[2]

        if not success:
            basic.append(f"{YELLOW}{read_program(program[0],False).index(line)} {RED}[Error] " + line + f"{RESET}")
            error = True
            continue

        if line_type == 0:
            basic.append(f"Input \"{params[1]}\",{params[0]}")
        elif line_type == 1:
            basic.append(f"Input \"{params[1]}\",{params[0]}")
        elif line_type == 2:
            basic.append(f"Input \"{params[1]}\",{params[0]}")
        elif line_type == 3:
            basic.append(f"{params[1]}→{params[0]}")
        elif line_type == 4:
            basic.append("ClrHome")
        elif line_type == 5:
            basic.append(f"Wait {params[0]}")
        elif line_type == 6:
            basic.append(f"Disp {params[0][0:-1]}")
        elif line_type == 7:
            basic.append(f"Output({params[0]}")
        elif line_type == 8:
            basic.append(f"Disp {params[0][0:-1]}")
        elif line_type == 9:
            basic.append(f"Goto {params[0]}")
        elif line_type == 10:
            basic.append(f"Lbl {params[0]}")
        elif line_type == 11:
            basic.append(f"Pause {params[0]}")
        elif line_type == 12:
            basic.append(f"Stop")
        elif line_type == 13:
            basic.append(parse_menu_func(params[0]))
    
    # replacements
    for i in range(len(basic)):
        line = basic[i]
        if "**" in line:
            basic[i] = basic[i].replace("**","^")
        if "Sqrt(" in line:
            basic[i] = basic[i].replace("Sqrt(","√(")
        if "PI" in line:
            basic[i] = basic[i].replace("PI","π")

    if error:
        print(f"{RED}Segmentation Fault{RESET}")
    else:
        print(f"{GREEN}Compilation Succeeded{RESET}")

    return basic

def basic_to_binary(program:list[str]) -> str:
    binary:list[str] = []
    # break everything up into chunks
    for line in program:
        if "[Error]" in line:
            binary.append("Stop")
        elif "(" in line or "," in line or " " in line: # if it's a complex command
            current:str = "" # current piece

            # break apart pieces differently, depending if we're in a string or not
            inquotes = False
            exclude:str = ""

            for char in line:
                if char == '"': inquotes = not inquotes # if we hit a string, toggle
                if not inquotes: exclude = " " # decide parameters for excluding depending on string/or not
                else: exclude = ""

                if not char in "," + exclude: # we want to split accross commas (and sometimes spaces)
                    current += char

                if char in "(,"+exclude:
                    binary.append(current) # break apart
                    current = ""

                    if char == ",": # we want to re-add the comma into a different piece (not the space)
                        binary.append(",")

            if current != "": # add the last piece if there is any
                binary.append(current)
        else: # if its a simple command
            binary.append(line)
        
        binary.append("linebreak")

    binary.pop() # remove last linebreak

    # with everything broken up, translate to binary
    for i in range(len(binary)):
        line = binary[i]
        if line in commands: # converts basic commands
            binary[i] = hex_commands[commands.index(line)]
        else: # translates everything else
            translated:str = ""
            for char in binary[i]:
                if char.upper() in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    # TI is standard with Alphanumeric keys
                    translated += to_hex_2byte_multiple(char.upper())
                else:
                    # TI absolutely fricking hates symbols though
                    translated += hex_chars[chars.index(char.upper())]
            binary[i] = translated

    # reassemble into one long binary string
    output:str = ""
    for line in binary:
        output += line

    return output.strip() # remove spaces

def compile(filename:str):
    # read the relevant parts of the Python Program
    # convert the Python program to a TI-Basic Program
    # convert the TI-Basic Program to TI-compatible binary code
    python_program = read_program(filename)
    basic_program = python_to_basic(python_program)
    binary = basic_to_binary(basic_program)
    return binary

def display_binary(binary:str):
    display_binary:str = ""
    for i in range(int(len(binary)/2)):
        byte = binary[i*2] + binary[i*2+1]
        display_binary += byte + " "
        if byte == "3F":
            display_binary += "\n"
    display_basic:str = ""
    for item in basic_program:
        display_basic += item + "\n"
    print(display_basic)

def detect_form(form_line:str):
    blocks:list[str] = []
    appending:bool = False
    for char in form_line:
        if char == "}":
            appending = False
        elif char == "{":
            appending = True
            blocks.append("")
        elif appending:
            blocks[-1] += char
    #print(blocks)
    return blocks

def match_form(form_line:str,line:str):
    blocks:list[str] = detect_form(form_line)
    results:list[str] = []
    match_line = line.strip()
    char_idx = 0
    success = True

    for key in blocks:
        if key == "/varname":
            valid_var_names = "abcdefghijklmnopqrstuvwxyzθ"
            if match_line[char_idx] in valid_var_names and match_line[char_idx+1] not in valid_var_names:
                results.append(match_line[char_idx])
                char_idx += 1
            else:
                #print("form not good :(")
                success = False
                return (False,[""])
        elif key == "/space":
            while match_line[char_idx] == " ": char_idx += 1
        elif key == "/value":
            results.append("")
            while char_idx < len(match_line):
                results[-1] += match_line[char_idx]
                char_idx += 1
        elif key == "/string":
            if match_line[char_idx] != "\"": return (False,[""])
            char_idx += 1
            results.append("")
            while match_line[char_idx] != "\"":
                results[-1] += match_line[char_idx]
                char_idx += 1
        elif key == "/label":
            if not match_line[char_idx] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": return (False,[""])
            char_idx += 1
            if not match_line[char_idx] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789": return (False,[""])
            char_idx += 1
            results.append(match_line[char_idx-2] + match_line[char_idx-1])
        else:
            for keychar in key:
                if keychar != match_line[char_idx]:
                    #print("form not good :(")
                    success = False
                    return (False,[""])
                else:
                    char_idx += 1

    #print(results)
    return (success,results)

def match_many_forms(many_forms:list[str], line:str):
    for i in range(len(many_forms)):
        form = many_forms[i]
        out = match_form(form,line)
        if not out[0]: continue
        return (True,i,out[1])
    return (False,-1,[""])


if __name__ == "__main__":
    # sample run
    target_name = "programs/sample.py"
    python_program = read_program(target_name)
    basic_program = python_to_basic(python_program,)
    binary = basic_to_binary(basic_program)

    print(f"{YELLOW}Decompiled Binary:{RESET}")
    display_binary(binary)