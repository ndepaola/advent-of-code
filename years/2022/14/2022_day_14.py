from typing import Iterable, TypeAlias

Point: TypeAlias = tuple[int, int]  # x, y
Cave: TypeAlias = dict[Point, bool]  # (x, y) => is this cell filled?


def draw_line(start: Point, end: Point) -> list[Point]:
    # super naive solution which handles drawing straight lines in cardinal directions only
    return [
        (x, y)
        for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1)
        for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1)
    ]


def read_input_file(file_name: str = "input.txt") -> Cave:
    cave: Cave = {}
    with open(file_name, "r") as f:
        for line in f.readlines():
            split_line = line.strip().split(" -> ")  # handle each continuous line of rock separately
            for i in range(len(split_line) - 1):  # fill the cave between each adjacent pair of coordinates
                start, end = split_line[i].split(","), split_line[i + 1].split(",")
                cave = cave | {
                    point: True for point in draw_line((int(start[0]), int(start[1])), (int(end[0]), int(end[1])))
                }
        return cave


def get_possible_sand_movements(point: Point) -> Iterable[Point]:
    yield point[0], point[1] + 1  # directly down
    yield point[0] - 1, point[1] + 1  # diagonally down and left
    yield point[0] + 1, point[1] + 1  # diagonally down and right


def simulate_cave(cave: Cave, sand_source: Point, bottomless_void: bool) -> int:
    sand_block_count, mutated_cave = 0, {**cave}
    cave_height = max([x[1] for x in mutated_cave.keys()]) + 1
    while True:
        sand_block = sand_source
        if mutated_cave.get(sand_block, False):
            return sand_block_count  # the cave has filled with sand
        mutated_cave[sand_block] = True
        while True:
            exhausted_all_movement_options = True
            for new_point in get_possible_sand_movements(sand_block):
                if mutated_cave.get(new_point, False) is False:
                    if new_point[1] > cave_height:
                        if bottomless_void:
                            return sand_block_count
                        else:
                            break
                    # the sand block can move into this position!
                    mutated_cave[new_point], mutated_cave[sand_block] = True, False
                    sand_block = new_point
                    exhausted_all_movement_options = False
                    break
            if exhausted_all_movement_options:
                sand_block_count += 1
                break


if __name__ == "__main__":
    c = read_input_file("input.txt")
    print(
        f"The number of sand blocks that can fall when the cave is a bottomless pit is "
        f"{simulate_cave(c, (500, 0), bottomless_void=True)}."
    )
    print(
        f"The number of sand blocks that can fall when the cave is not a bottomless pti is "
        f"{simulate_cave(c, (500, 0), bottomless_void=False)}."
    )
