commands = ["linebreak","ClrHome","Wait","Output(","Input","Disp","√("]
hex_commands = ["3F","E1","EF 96","E0","DC","DE","BC"]

chars =     [",",'"'," ",".",":","-","+","*","/","=","(",")","→"]
hex_chars = ["2B","2A","29","3A","3E","71","70","82","83","6A","10","11","04"]

def to_hex_2byte_multiple(value:str|int|bytes|bytearray) -> str:
    # for standard conversion to hex
    if isinstance(value, int):
        hex_str = f"{value:X}"
    elif isinstance(value, str):
        hex_str:str = ""
        for char in value:
            hex_str += char.encode().hex().upper()
    elif isinstance(value, (bytes, bytearray)):
        hex_str = value.hex().upper()
    else:
        raise TypeError("Unsupported type")

    pad = (-len(hex_str)) % 2
    return "0" * pad + hex_str

def read_program(name:str) -> list[str]:
    # filters out unecessary header code for python file
    program:list[str] = []
    try:
        with open(name, 'r', encoding='utf-8') as f:
            lines_list: list[str] = f.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{target_name}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    started = False
    for line in lines_list:
        if not started and line == "# __start__ #\n":
            started = True
            continue
        if started and line[0] != "#" and line.strip() != "":
            program.append(line.strip())
    return program

def python_to_basic(program:list[str]) -> list[str]:
    # reformat python into TI-Basic
    # after this stage, all code should be copy-pasteable into TI-Connect CE program editor
    basic:list[str] = []
    for line in program:
        if line == "ClrHome()":
            basic.append("ClrHome")
        elif line[0:5] == f"Wait(":
            basic.append(f"Wait {line[5]}")
        elif line[1] == "=":
            if line[2:8] == "Input(":
                basic.append(f"Input {line[8:len(line)-1]},{line[0].upper()}")
            else:
                basic.append(f"{line[2:len(line)]}→{line[0].upper()}")
        elif line[2] == "=":
            if line[4:10] == "Input(":
                basic.append(f"Input {line[10:len(line)-1]},{line[0].upper()}")
            else:
                basic.append(f"{line[4:len(line)]}→{line[0].upper()}")
        elif line[0:5] == "Disp(":
            basic.append(f"Disp {line[5:len(line)-1]}")
        elif line[0:7] == "Output(":
            basic.append(f"Output({line[7:len(line)-1]}")
        elif line[0:6] == "print(":
            basic.append(f"Disp {line[6:len(line)-1]}")
        else:
            basic.append(line)
    
    # replacements
    for i in range(len(basic)):
        line = basic[i]
        if "Sqrt(" in line:
            basic[i] = basic[i].replace("Sqrt(","√(")

    return basic

def basic_to_binary(program:list[str]) -> str:
    binary:list[str] = []
    # break everything up into chunks
    for line in program:
        if "(" in line or "," in line or " " in line: # if it's a complex command
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

if __name__ == "__main__":
    # sample run
    target_name = "sample.py"
    binary:str = compile(target_name)
    display:str = ""
    for i in range(int(len(binary)/2)):
        byte = binary[i*2] + binary[i*2+1]
        display += byte + " "
        if byte == "3F":
            display += "\n"
    print(display)