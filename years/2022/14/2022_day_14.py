from typing import Iterable, TypeAlias

Point: TypeAlias = tuple[int, int]  # x, y
Cave: TypeAlias = set[Point]  # (x, y) => is this cell filled?


def draw_line(start: Point, end: Point) -> set[Point]:
    # super naive solution which handles drawing straight lines in cardinal directions only
    return {
        (x, y)
        for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1)
        for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1)
    }


def read_input_file(file_name: str = "input.txt") -> Cave:
    cave: Cave = set()
    with open(file_name, "r") as f:
        for line in f.readlines():
            split_line = line.strip().split(" -> ")  # handle each continuous line of rock separately
            for i in range(len(split_line) - 1):  # fill the cave between each adjacent pair of coordinates
                start, end = split_line[i].split(","), split_line[i + 1].split(",")
                cave |= draw_line((int(start[0]), int(start[1])), (int(end[0]), int(end[1])))
        return cave


def get_possible_sand_movements(point: Point) -> Iterable[Point]:
    yield point[0], point[1] + 1  # directly down
    yield point[0] - 1, point[1] + 1  # diagonally down and left
    yield point[0] + 1, point[1] + 1  # diagonally down and right


def simulate_cave(cave: Cave, sand_source: Point, bottomless_void: bool) -> int:
    sand_block_count, mutated_cave = 0, {*cave}
    cave_height = max([x[1] for x in mutated_cave]) + 1
    while True:
        sand_block = sand_source
        if sand_block in mutated_cave:
            return sand_block_count  # the cave has filled with sand
        mutated_cave.add(sand_block)
        while True:
            exhausted_all_movement_options = True
            for new_point in get_possible_sand_movements(sand_block):
                if new_point not in mutated_cave:
                    if new_point[1] > cave_height:
                        if bottomless_void:
                            return sand_block_count
                        else:
                            break
                    # the sand block can move into this position!
                    mutated_cave.remove(sand_block)
                    mutated_cave.add(new_point)
                    sand_block = new_point
                    exhausted_all_movement_options = False
                    break
            if exhausted_all_movement_options:
                sand_block_count += 1
                break


if __name__ == "__main__":
    c = read_input_file("input.txt")
    print(
        f"After {simulate_cave(c, (500, 0), bottomless_void=True)} blocks of sand fall, any further blocks of sand "
        f"will fall into the bottomless pit."
    )
    print(f"It takes {simulate_cave(c, (500, 0), bottomless_void=False)} blocks of sand to completely fill the cave.")
