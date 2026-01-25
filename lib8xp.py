from typing import BinaryIO
# formats for the .8xp file format

def integer_to_hex(length:int,value:int) -> str:
    return value.to_bytes(length, byteorder="little").hex()

def integer_to_hex_general(value:int) -> str:
    return value.to_bytes((value.bit_length() + 7) // 8, "little").hex()

def write_hex(hex:str, file:BinaryIO) -> None:
    binary = bytes.fromhex(hex.strip())
    file.write(binary)

def gen_checksum(hex:str) -> str:
    total:int = 0
    for i in range(int(len(hex)/2)):
        current_byte:str = hex[i*2] + hex[i*2+1]
        total += int(current_byte,16)

    total_hex = integer_to_hex_general(total)

    return total_hex[0:4]

def to_8xp_binary(code:str,TI_name:str) -> str:
    header_bytes = 55
    meta_bytes = 19
    checksum_bytes = 2
    total_bytes:int = header_bytes + meta_bytes + checksum_bytes + int(len(code.replace(" ",""))/2)

    # --- values --- #
    body_bytes: int = total_bytes - header_bytes - meta_bytes - checksum_bytes
    meta_body_bytes:int = meta_bytes + body_bytes
    body_checksum_bytes:int = body_bytes + checksum_bytes

    # header
    signiature = "2A 2A 54 49 38 33 46 2A" # always **TI83F*
    signiature2 = "1A 0A" # always 1A 0A
    mystery_byte = "0A" # supposedly made with TI Connect CE
    comment = "43 72 65 61 74 65 64 20 62 79 20 50 79 2D 42 61 73 69 63 20 43 6F 6D 70 69 6C 65 72 20 56 65 72 73 69 6F 6E 20 31 2E 30 00 00" # "Created by Py-Basic Compiler Version 1.0" - 42 bytes
    meta_body_length: str = integer_to_hex(2,meta_body_bytes)
    #metadata
    flag = "0D" # most common
    unknown = "00" # most common
    body_checksum_length: str = integer_to_hex(2,body_checksum_bytes)
    file_type = "05" # normal program
    program_name: str = TI_name.encode("utf-8").hex()
    while len(program_name) < 16: program_name += "00" # ensure program name is 8 bytes long
    version = "00" # most common
    is_archived = "00" # 00 for unarchived and 80 for archived
    body_checksum_length2: str = integer_to_hex(2,body_checksum_bytes)
    body_length: str = integer_to_hex(2,body_bytes)

    # four major sections
    header_hex: str = signiature + signiature2 + mystery_byte + comment + meta_body_length
    metadata_hex: str = flag + unknown + body_checksum_length + file_type + program_name + version + is_archived + body_checksum_length2 + body_length
    program_hex:str = code.replace(" ","")
    checksum_hex: str = gen_checksum(metadata_hex + program_hex)

    entire_file: str = (header_hex + metadata_hex + program_hex + checksum_hex).upper().replace(" ","")
    return entire_file

def create_file_from_binary(filename:str,filedata:str) -> None:
    with open(f"{filename}.8xp", "wb") as f:
        write_hex(filedata,f)

if __name__ == "__main__":
    # --- sample variables --- #
    program_name = "SERENITY"
    file_name = "serenity"
    program_code = "E1 3F E0 35 2B 31 33 2B 2A 53 54 41 52 54 49 4E 47 29 53 45 52 45 4E 49 54 59 2A"
    binary: str = to_8xp_binary(program_code,program_name)
    print(binary)
    create_file_from_binary(file_name,binary)