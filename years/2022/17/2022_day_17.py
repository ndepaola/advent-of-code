from typing import TypeAlias

Point: TypeAlias = tuple[int, int]  # x, y


def read_input_file(file_name: str = "input.txt") -> list[int]:
    with open(file_name, "r") as f:
        return list(map(lambda x: {"<": -1, ">": 1}[x], f.read().strip()))


def shift_lateral(p: Point, delta: int) -> Point:
    return p[0] + delta, p[1]


def shift_vertical(p: Point, delta: int) -> Point:
    return p[0], p[1] + delta


def stringify_cave(rocks_in_cave: set[Point], floor_height: int, width: int, rows_from_top: int | None = None) -> str:
    # turns the cave into a string similar ot the examples in the advent of code question.
    # optionally, this will only print the first `n` rows of the cave (used for identifying the repeating pattern).
    cave_string = ""
    for y in range(floor_height, 0 if rows_from_top is None else floor_height - rows_from_top, -1):
        for x in range(width):
            cave_string += "#" if (x, y) in rocks_in_cave else "."
        cave_string += "\n"
    return cave_string


def get_rocks() -> tuple[set[Point], ...]:
    return (
        {(0, 0), (1, 0), (2, 0), (3, 0)},  # -
        {(1, 0), (0, -1), (1, -1), (2, -1), (1, -2)},  # +
        {(0, -2), (1, -2), (2, -2), (2, -1), (2, 0)},  # ⅃
        {(0, 0), (0, -1), (0, -2), (0, -3)},  # I
        {(0, 0), (0, -1), (1, 0), (1, -1)},  # □
    )


def get_rock_dimensions(rocks: tuple[set[Point], ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    rock_widths = []
    rock_heights = []
    for rock in rocks:
        x, y = zip(*rock)
        rock_widths.append(max(x) - min(x) + 1)
        rock_heights.append(max(y) - min(y) + 1)
    return tuple(rock_widths), tuple(rock_heights)


def simulate_rocks_falling(
    rock_count: int,
    jets: list[int],
    pattern_preamble: int = 50,
    width: int = 7,
    rock_x_offset: int = 2,
    rock_y_offset: int = 3,
) -> int:
    rocks = get_rocks()
    rock_widths, rock_heights = get_rock_dimensions(rocks)

    # coupla initialisation things
    jet_index = -1
    floor_height = 0
    rocks_in_cave: set[Point] = set()
    cave_strings: list[str] = []
    height_offset_for_all_patterns = 0
    height_per_rock_number: dict[int, int] = {}
    pattern_reduced = False

    rock_number = 0
    while rock_number < rock_count:
        rock_index = rock_number % len(rocks)
        rock_width = rock_widths[rock_index]
        rock_height = rock_heights[rock_index]
        rock_x_position = rock_x_offset
        rock_y_position = floor_height + rock_y_offset + rock_height
        rock = {shift_vertical(shift_lateral(x, rock_x_position), rock_y_position) for x in rocks[rock_index]}
        in_motion = True

        while in_motion:
            jet_index = (jet_index + 1) % len(jets)
            jet = jets[jet_index]

            # attempt to move laterally
            if 1 <= rock_x_position + (rock_width if jet > 0 else 0) < width:
                shifted_rock = {shift_lateral(x, jet) for x in rock}
                if not shifted_rock & rocks_in_cave:
                    rock = shifted_rock
                    rock_x_position += jet

            # attempt to move down
            dropped_rock = {shift_vertical(x, -1) for x in rock}
            if (not dropped_rock & rocks_in_cave) and rock_y_position - rock_height > 0:
                # there's space to move this rock down
                rock = dropped_rock
                rock_y_position -= 1
            else:
                # this rock is at rest
                floor_height = max(floor_height, rock_y_position)
                rocks_in_cave |= rock
                break

        if rock_number > pattern_preamble:
            cave_string = stringify_cave(rocks_in_cave, floor_height, width, rows_from_top=pattern_preamble)
            if (
                not pattern_reduced
                and len(
                    numbers_that_match_the_pattern := [
                        i for i, previous_cave_string in enumerate(cave_strings) if previous_cave_string == cave_string
                    ]
                )
                > 1
            ):
                # a repeating pattern has been identified between the cave in this state and a previous state
                # we can calculate the following information between that state and this state:
                # * the number of rocks that comprise the repeating pattern
                # * the height of the repeating pattern
                # with this information, we can skip all instances of the pattern and jump to the end of the simulation
                pattern_rocks = rock_number - max(numbers_that_match_the_pattern) - pattern_preamble - 1
                pattern_height = (
                    floor_height - height_per_rock_number[max(numbers_that_match_the_pattern) + pattern_preamble + 1]
                )
                number_of_patterns_to_skip = (rock_count - rock_number) // pattern_rocks
                height_offset_for_all_patterns = number_of_patterns_to_skip * pattern_height  # add to final answer
                rock_count -= number_of_patterns_to_skip * pattern_rocks
                pattern_reduced = True  # avoid performing this optimisation more than once
            cave_strings.append(cave_string)
        height_per_rock_number[rock_number] = floor_height
        rock_number += 1
    return floor_height + height_offset_for_all_patterns


if __name__ == "__main__":
    j = read_input_file("input.txt")
    print(f"After 2022 rocks have fallen, the height of the rock tower is {simulate_rocks_falling(2022, j)}.")
    print(
        f"After literally one trillion rocks have fallen, the height of the rock tower is "
        f"{simulate_rocks_falling(1_000_000_000_000, j)}."
    )
