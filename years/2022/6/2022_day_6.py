from builtins import bytes
from functools import partial


def identify_characters_before_start_of_marker(marker_length: int, file_name: str = "input.txt") -> int:
    register: list[bytes] = []
    counter = 1
    with open(file_name, "rb") as f:
        for character in iter(partial(f.read, 1), b""):
            if len(register) >= marker_length:
                register.pop(0)
            register.append(character)
            if len(set(register)) == marker_length:
                break
            counter += 1
    return counter


if __name__ == "__main__":
    print(
        f"The number of characters before the 4-character marker is "
        f"{identify_characters_before_start_of_marker(marker_length=4)}."
    )
    print(
        f"The number of characters before the 14-character marker is "
        f"{identify_characters_before_start_of_marker(marker_length=14)}."
    )
