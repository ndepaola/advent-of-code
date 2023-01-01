def read_input_file(file_name: str = "input.txt") -> list[int]:
    with open(file_name, "r") as f:
        return [int(stripped_line) for line in f.readlines() if (stripped_line := line.strip())]


def mix(items: list[int], repetitions: int) -> list[int]:
    indexes = list(range(len(items)))
    for _ in range(repetitions):
        for i, item in enumerate(items):
            item_index = indexes.index(i)
            value = indexes.pop(item_index)
            indexes.insert((item_index + item - 1) % len(indexes) + 1, value)
    return [items[i] for i in indexes]


def find_grove_coordinates_sum(mixed_items: list[int], value_to_find: int = 0) -> int:
    start_index = mixed_items.index(value_to_find)
    return sum([mixed_items[(start_index + i - 1) % len(mixed_items) + 1] for i in range(1000, 4000, 1000)])


if __name__ == "__main__":
    encrypted = read_input_file("input.txt")
    print(f"The sum of the grove coordinates after mixing once is {find_grove_coordinates_sum(mix(encrypted, 1))}.")
    print(
        f"The sum of the grove coordinates after applying the decryption key then mixing ten times is "
        f"{find_grove_coordinates_sum(mix([number * 811589153 for number in encrypted], 10))}."
    )
