import re
from typing import Callable, TypeAlias

Point: TypeAlias = tuple[int, int]  # x, y
Map: TypeAlias = dict[Point, bool]  # point => is this point traversable (i.e. not a wall)?
Commands: TypeAlias = list[str | int]  # str for direction to turn in, int for number of tiles to move
EdgeAdjacencies: TypeAlias = dict[tuple[Point, int], tuple[Point, int]]  # (point, direction) => (point, direction)

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


def get_edge_adjacencies() -> EdgeAdjacencies:
    # TODO: hardcoding these mappings for my input for now. might come back to this puzzle later and solve it properly.
    mapping = (
        {((var_1, 49), 1): ((99, var_2), 2) for var_1, var_2 in zip(range(100, 149 + 1), range(50, 99 + 1))}
        | {((149, var_1), 0): ((99, var_2), 2) for var_1, var_2 in zip(range(0, 49 + 1), range(149, 100 - 1, -1))}
        | {((var_1, 0), 3): ((0, var_2), 0) for var_1, var_2 in zip(range(50, 99 + 1), range(150, 199 + 1))}
        | {((var_1, 149), 1): ((49, var_2), 2) for var_1, var_2 in zip(range(50, 99 + 1), range(150, 199 + 1))}
        | {((var_1, 100), 3): ((50, var_2), 0) for var_1, var_2 in zip(range(0, 49 + 1), range(50, 99 + 1))}
        | {((50, var_1), 2): ((0, var_2), 0) for var_1, var_2 in zip(range(0, 49 + 1), range(149, 100 - 1, -1))}
        | {((var_1, 0), 3): ((var_2, 199), 3) for var_1, var_2 in zip(range(100, 149 + 1), range(0, 49 + 1))}
    )
    reversed_mapping = {}  # ensure the edges can be traversed both ways
    for key, value in mapping.items():
        reversed_mapping[(value[0], (value[1] + 2) % len(DIRECTIONS))] = (key[0], (key[1] + 2) % len(DIRECTIONS))
    return mapping | reversed_mapping


def wrap_around_flat_map(map_: Map, position: Point, direction: int) -> tuple[Point, int]:
    temporary_direction = (direction + 2) % len(DIRECTIONS)  # about face
    temporary_position = position
    while True:
        new_temporary_position = move_in_direction(temporary_position, temporary_direction)
        if map_.get(new_temporary_position, None) is None:
            break
        temporary_position = new_temporary_position
    if map_.get(temporary_position, False) is True:
        return temporary_position, direction
    return position, direction  # the wrapped-around position is not traversable


def wrap_around_cube_map(map_: Map, position: Point, direction: int) -> tuple[Point, int]:
    adjacencies = get_edge_adjacencies()
    assert (position, direction) in adjacencies.keys(), "edge adjacency map is incomplete"
    if map_.get(adjacencies[(position, direction)][0], False) is True:
        return adjacencies[(position, direction)]
    return position, direction  # the wrapped-around position is not traversable


def traverse(
    map_: Map, commands: Commands, wrap_around_callable: Callable[[Map, Point, int], tuple[Point, int]]
) -> int:
    position = min([x for x in map_.keys() if x[1] == 0])  # leftmost tile in top row
    direction = 0  # east
    for counter, command in enumerate(commands):
        if isinstance(command, str):
            # rotate
            direction = (direction + {"R": 1, "L": -1}[command]) % len(DIRECTIONS)
        else:
            # move
            for _ in range(command):
                new_position = move_in_direction(position, direction)
                match map_.get(new_position, None):
                    case True:  # new position is within map and is traversable
                        position = new_position
                    case False:  # new position is within map and is not traversable
                        break
                    case None:  # new position is outside map
                        position, direction = wrap_around_callable(map_, position, direction)
    return 1000 * (position[1] + 1) + 4 * (position[0] + 1) + direction


if __name__ == "__main__":
    m, c = read_input_file("input.txt")
    print(f"The final password when the map is flat is {traverse(m, c, wrap_around_flat_map)}.")
    print(f"The final password when the map is a cube is {traverse(m, c, wrap_around_cube_map)}.")
