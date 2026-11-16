from src.assembler import assemble


def test_commands():
    instructions = assemble("tests/program.yaml")

    expected = [
        (0, 123, 4),
        (1, 0, 1),
        (5, 1, 0),
        (6, 3, 7),
    ]

    actual = [
        (cmd["A"], cmd["B"], cmd["C"])
        for cmd in instructions
    ]

    assert actual == expected


if __name__ == "__main__":
    test_commands()
    print("Все тесты пройдены!")