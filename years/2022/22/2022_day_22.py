import re
from typing import TypeAlias

Point: TypeAlias = tuple[int, int]  # x, y
Map: TypeAlias = dict[Point, bool]  # point => is this point traversable (i.e. not a wall)?
Commands: TypeAlias = list[str | int]  # str for direction to turn in, int for number of tiles to move

DIRECTIONS: list[Point] = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # east, south, west, north. top-left is (0, 0).


def add_points(point_a: Point, point_b: Point) -> Point:
    return point_a[0] + point_b[0], point_a[1] + point_b[1]


def move_in_direction(point: Point, direction: int) -> Point:
    return add_points(point, DIRECTIONS[direction])


def read_input_file(file_name: str = "input.txt") -> tuple[Map, Commands]:
    with open(file_name, "r") as f:
        map_text, commands_text = f.read().split("\n\n")
        commands = [int(x) if x.strip().isdigit() else x for x in re.split(r"([LR])", commands_text) if x.strip()]
        map_: Map = {}
        for y, line in enumerate(map_text.splitlines()):
            for x, character in enumerate(line):
                if character.strip() in [".", "#"]:
                    map_[(x, y)] = character.strip() == "."
                elif character != " ":
                    raise Exception

        return map_, commands


def traverse(map_: Map, commands: Commands) -> None:
    position = min([x for x in map_.keys() if x[1] == 0])  # leftmost tile in top row
    direction = 0  # east
    for command in commands:
        if isinstance(command, str):
            # rotate
            direction = (direction + {"R": 1, "L": -1}[command]) % len(DIRECTIONS)
        else:
            # move
            for _ in range(command):
                new_position = move_in_direction(position, direction)
                new_position_in_map = map_.get(new_position, None)
                if new_position_in_map is True:
                    position = new_position
                elif new_position_in_map is None:
                    # wrap around map
                    temporary_direction = (direction + 2) % len(DIRECTIONS)  # about face
                    temporary_position = position
                    while True:
                        new_temporary_position = move_in_direction(temporary_position, temporary_direction)
                        if map_.get(new_temporary_position, None) is None:
                            break
                        temporary_position = new_temporary_position
                    if map_.get(temporary_position, False) is True:
                        position = temporary_position
                else:  # new_position_in_map is False
                    break
    print(1000 * (position[1] + 1) + 4 * (position[0] + 1) + direction)


if __name__ == "__main__":
    m, c = read_input_file("input.txt")
    traverse(m, c)
