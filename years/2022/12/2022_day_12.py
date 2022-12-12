import dataclasses
import time
from queue import PriorityQueue
from typing import Any, TypeAlias

Point: TypeAlias = tuple[int, int]  # x, y
HeightMap: TypeAlias = dict[Point, int]  # point => elevation


def get_value_for_character(character: str) -> int:
    assert len(character) == 1, f"Attempted to get the value of a character but the string was {len(character)} long"
    return ord(character) - 96


def heuristic(source: Point, target: Point) -> int:
    # a simple admissible heuristic for the cost of moving from `source` to `target` - Manhattan distance :)
    return abs(source[0] - target[0]) + abs(source[1] + target[1])


def possible_moves(source: Point, heightmap: HeightMap, height_delta: int = 1) -> list[Point]:
    # return a list of possible moves from `source`, taking `heightmap` into account
    moves = []
    for possible_move in (
        (source[0], source[1] + 1),  # up
        (source[0], source[1] - 1),  # down
        (source[0] - 1, source[1]),  # left
        (source[0] + 1, source[1]),  # right
    ):
        if possible_move in heightmap.keys() and heightmap[possible_move] - heightmap[source] <= height_delta:
            moves.append(possible_move)
    return moves


def read_input_file(file_name: str = "input.txt") -> tuple[HeightMap, Point, Point]:  # map, start, target
    heightmap = {}
    start = None
    target = None
    with open(file_name, "r") as f:
        for y, line in enumerate(f.readlines()):
            for x, character in enumerate(line):
                if character == "S":
                    assert start is None, "multiple starts in input!"
                    start = (x, y)
                    character = "a"
                elif character == "E":
                    assert target is None, "multiple targets in input!"
                    target = (x, y)
                    character = "z"
                heightmap[(x, y)] = get_value_for_character(character)
    assert start is not None and target is not None, "start and end not specified in input!"
    return heightmap, start, target


@dataclasses.dataclass
class HeuristicPoint:
    h: int = dataclasses.field()
    point: Point = dataclasses.field()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, HeuristicPoint) and self.h == other.h

    def __lt__(self, other: Any) -> bool:
        return isinstance(other, HeuristicPoint) and self.h < other.h


def reconstruct_path(point: Point, previous_point_map: dict[Point, Point]) -> list[Point]:
    if point in previous_point_map.keys():
        return [point] + reconstruct_path(previous_point_map[point], previous_point_map)
    return [point]


def a_star_search(start: Point, target: Point, heightmap: HeightMap) -> list[Point]:
    frontier: PriorityQueue[HeuristicPoint] = PriorityQueue()
    frontier.put(HeuristicPoint(point=start, h=heuristic(start, target)))
    previous_point: dict[Point, Point] = {}
    g_score: dict[Point, int | None] = {start: 0}  # none represents infinite
    while True:
        if frontier.empty():
            return []  # infeasible given the starting point and possible moves
        current_point = frontier.get()
        if current_point.point == target:
            return reconstruct_path(current_point.point, previous_point)
        moves = possible_moves(current_point.point, heightmap)
        for move in moves:
            # coupla type ignores here because mypy thinks a.get(thing, number) foc whatever reason? might fix later
            tentative_score = g_score.get(current_point.point, 1_000_000) + 1  # type: ignore
            if tentative_score < g_score.get(move, 1_000_000):  # type: ignore
                previous_point[move] = current_point.point
                g_score[move] = tentative_score
                frontier.put(HeuristicPoint(point=move, h=heuristic(move, target) + tentative_score))


if __name__ == "__main__":
    t0 = time.time()  # measure running time of part a
    hm, start_point, end_point = read_input_file("input.txt")
    optimal_path = a_star_search(start_point, end_point, hm)
    print(
        f"Starting from {start_point}, the optimal path is {len(optimal_path)-1} steps long. "
        f"This was computed in roughly {round(time.time() - t0, 2)} seconds."
    )
    t1 = time.time()  # measure running time of part b
    possible_start_points = [key for key, value in hm.items() if value == 1]
    possible_answers = []
    for possible_start_point in possible_start_points:
        if len(possible_path := a_star_search(possible_start_point, end_point, hm)) > 0:
            possible_answers.append(len(possible_path) - 1)
    print(
        f"Starting from any point of elevation 1, the optimal path is {min(possible_answers)} steps long. "
        f"This was computed in roughly {round(time.time() - t1, 2)} seconds."
    )
