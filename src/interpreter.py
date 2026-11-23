import argparse


MEMORY_SIZE = 2048
REGISTER_COUNT = 8
INSTRUCTION_SIZE = 4


def create_memory():
    """Создать общую память"""
    return [0] * MEMORY_SIZE


def create_registers():
    """Создать восемь регистров"""
    return [0] * REGISTER_COUNT

def load_program(memory, filename):
    """Загрузить машинные команды"""
    with open(filename, "rb") as file:
        data = file.read()
    if len(data) % INSTRUCTION_SIZE != 0:
        raise ValueError("Размер программы не кратен 4 байтам")
    command_count = len(data) // INSTRUCTION_SIZE
    if command_count > len(memory):
        raise ValueError("Программа не помещается в память")
    for i in range(command_count):
        start = i * INSTRUCTION_SIZE
        command_bytes = data[start:start + INSTRUCTION_SIZE]
        memory[i] = int.from_bytes(
            command_bytes, byteorder="little"
        )
    return command_count

def decode_instruction(value):
    """Декодировать машинную команду"""
    a = value & 0b111
    if a == 0:
        b = (value >> 3) & 0xFFFFFF
        c = (value >> 27) & 0b111
    elif a in (1, 5, 6):
        b = (value >> 3) & 0b111
        c = (value >> 6) & 0b111
    else:
        raise ValueError(f"Неизвестный код операции: {a}")
    return {"A": a, "B": b, "C": c}

def execute_instruction(command, memory, registers):
    """Выполнить инструкцию"""
    a = command["A"]
    b = command["B"]
    c = command["C"]
    if a == 0:
        registers[c] = b
    elif a == 1:
        registers[b] = memory[registers[c]]
    elif a == 5:
        memory[registers[b]] = registers[c]
    elif a == 6:
        memory[registers[b]] = int(
            memory[registers[b]] < registers[c]
        )

def run_program(memory, registers, command_count):
    """Выполнить все команды"""
    pc = 0
    while pc < command_count:
        value = memory[pc]
        command = decode_instruction(value)
        execute_instruction(command, memory, registers)
        pc += 1

def save_memory_dump(memory, filename, start, end):
    """Сохранить диапазон памяти в XML-файл"""
    if not 0 <= start <= end < len(memory):
        raise ValueError("Недопустимый диапазон памяти")
    with open(filename, "w", encoding="utf-8") as file:
        file.write('<?xml version="1.0" encoding="utf-8"?>\n')
        file.write("<memory>\n")
        for address in range(start, end + 1):
            file.write(
                f'    <cell address="{address}">'
                f'{memory[address]}</cell>\n'
            )
        file.write("</memory>\n")


def main():
    """Запустить интерпретатор через командную строку"""
    parser = argparse.ArgumentParser()
    parser.add_argument("binary_file", help="bin")
    parser.add_argument("dump_file", help="xml dump")
    parser.add_argument("start", type=int, help="start address")
    parser.add_argument("end", type=int, help="end address")
    args = parser.parse_args()
    memory = create_memory()
    registers = create_registers()
    command_count = load_program(memory, args.binary_file)
    run_program(memory, registers, command_count)
    save_memory_dump(memory, args.dump_file, args.start, args.end)
    print(f"Выполнено команд: {command_count}")
    print(f"Дамп сохранён в {args.dump_file}")


if __name__ == "__main__":
    main()