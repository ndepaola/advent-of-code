def read_input_file(file_name: str = "input.txt") -> list[int]:
    with open(file_name, "r") as f:
        return [int(line.strip()) for line in f.readlines() if line.strip()]


def mix(items: list[int], iterations: int) -> list[int]:
    mutated_items = [*items]
    indexes = list(range(len(items)))
    for _ in range(iterations):
        for i, item in enumerate(items):
            item_index = indexes.index(i)
            assert item == mutated_items[item_index]  # quick sanity check
            value = indexes.pop(item_index)
            indexes.insert((item_index + item - 1) % (len(indexes)) + 1, value)
            mutated_items = [items[i] for i in indexes]
    return mutated_items


def find_grove_coordinates_sum(mixed_items: list[int], value_to_find: int = 0) -> int:
    start_index = mixed_items.index(value_to_find)
    return sum(
        [mixed_items[(start_index + increment - 1) % len(mixed_items) + 1] for increment in range(1000, 4000, 1000)]
    )


if __name__ == "__main__":
    it = read_input_file("input.txt")
    print(f"The sum of the grove coordinates after mixing once is {find_grove_coordinates_sum(mix(it, 1))}.")
    print(
        f"The sum of the grove coordinates after applying the decryption key then mixing ten times is "
        f"{find_grove_coordinates_sum(mix([thing * 811589153 for thing in it], 10))}."
    )
