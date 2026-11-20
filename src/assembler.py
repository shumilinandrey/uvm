import argparse
import yaml


OPCODES = {
    "LOAD_CONST": 0,
    "READ_MEMORY": 1,
    "WRITE_MEMORY": 5,
    "LESS_THAN": 6,
}

MAX_REGISTER = 7
MAX_CONSTANT = (1 << 24) - 1
MIN_VALUE = 0
INSTRUCTION_SIZE = 4


def check_number(value, name, maximum):
    """Проверить, что поле является целым числом в нужном диапазоне."""
    if type(value) is not int:
        raise ValueError(f"Поле {name} должно быть целым числом")
    if not MIN_VALUE <= value <= maximum:
        raise ValueError(f"Поле {name} должно быть от 0 до {maximum}")
    return value


def parse_instruction(command):
    """Преобразовать одну YAML-команду в словарь с полями A, B, C."""
    if not isinstance(command, dict):
        raise ValueError("Команда должна быть словарём")
    if set(command) != {"operation", "B", "C"}:
        raise ValueError("Нужны поля operation, B и C")
    operation = command["operation"]
    if not isinstance(operation, str) or operation not in OPCODES:
        raise ValueError(f"Неизвестная операция: {operation}")
    maximum_b = MAX_CONSTANT if operation == "LOAD_CONST" else MAX_REGISTER
    return {
        "operation": operation,
        "A": OPCODES[operation],
        "B": check_number(command["B"], "B", maximum_b),
        "C": check_number(command["C"], "C", MAX_REGISTER),
    }


def assemble(source):
    """Прочитать YAML-файл и получить список инструкций."""
    with open(source, encoding="utf-8") as file:
        program = yaml.safe_load(file)
    if not isinstance(program, dict) or set(program) != {"commands"}:
        raise ValueError("В YAML должен быть только ключ commands")
    if not isinstance(program["commands"], list):
        raise ValueError("commands должен быть списком")
    instructions = []
    for number, command in enumerate(program["commands"], start=1):
        try:
            instructions.append(parse_instruction(command))
        except ValueError as error:
            raise ValueError(f"Команда {number}: {error}") from error
    return instructions


def print_instructions(instructions):
    """Вывести поля инструкций в тестовом режиме."""
    print(f"Количество команд: {len(instructions)}")
    for command in instructions:
        print(
            f"{command['operation']}: "
            f"A={command['A']}, B={command['B']}, C={command['C']}"
        )


def encode_instruction(command):
    """Закодировать инструкцию в четыре байта."""
    value = command["A"] | (command["B"] << 3)

    if command["operation"] == "LOAD_CONST":
        value |= command["C"] << 27
    else:
        value |= command["C"] << 6

    return value.to_bytes(INSTRUCTION_SIZE, byteorder="little")


def write_binary(instructions, output):
    """Записать последовательность инструкций в бинарный файл."""
    with open(output, "wb") as file:
        for command in instructions:
            file.write(encode_instruction(command))



def main():
    """Прочитать аргументы и выполнить ассемблирование."""
    parser = argparse.ArgumentParser(description="Ассемблер УВМ")
    parser.add_argument("source", help="Исходный YAML-файл")
    parser.add_argument("output", help="Выходной бинарный файл")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    try:
        instructions = assemble(args.source)
        print(f"Количество команд: {len(instructions)}")
        if args.test:
            for command in instructions:
                data = encode_instruction(command)
                print(data.hex(" ").upper())
        else:
            write_binary(instructions, args.output)
            print(f"Сохранено: {args.output}")
    except (OSError, ValueError, yaml.YAMLError) as error:
        parser.exit(1, f"Ошибка: {error}\n")



if __name__ == "__main__":
    main()