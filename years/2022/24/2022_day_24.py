import dataclasses
import heapq
import time
from typing import Any, TypeAlias

Point: TypeAlias = tuple[int, int]  # x, y. top-left is 0, 0.
Blizzard: TypeAlias = tuple[Point, int]  # starting position, direction (0, 1, 2, 3 => north, east, south west)


DELTAS = ((0, -1), (1, 0), (0, 1), (-1, 0))  # north, east, south, west


def read_input_file(
    file_name: str = "input.txt",
) -> tuple[Point, Point, set[Blizzard], int, int]:  # start, end, blizzards, width, height
    with open(file_name, "r") as f:
        start: Point | None = None
        end: Point | None = None
        blizzards: set[Blizzard] = set()
        for y, line in enumerate(f.readlines()):
            if stripped_line := line.strip():
                if (len(stripped_line) - 1) == stripped_line.count("#"):
                    if y == 0:
                        assert start is None
                        start = (stripped_line.index("."), y)
                    else:
                        assert end is None
                        end = (stripped_line.index("."), y)
                else:
                    blizzards |= {
                        ((x, y), {"^": 0, ">": 1, "v": 2, "<": 3}[ch])
                        for x, ch in enumerate(stripped_line)
                        if ch in ["^", ">", "v", "<"]
                    }
        assert start is not None and end is not None
        return start, end, blizzards, len(stripped_line), y + 1


def heuristic(source: Point, target: Point) -> int:
    # a simple admissible heuristic for the cost of moving from `source` to `target` - Manhattan distance :)
    return abs(source[0] - target[0]) + abs(source[1] - target[1])


def add_points(point_a: Point, point_b: Point) -> Point:
    return point_a[0] + point_b[0], point_a[1] + point_b[1]


def apply_magnitude_to_point(point: Point, magnitude: int) -> Point:
    return point[0] * magnitude, point[1] * magnitude


@dataclasses.dataclass(frozen=True)
class State:
    h: int = dataclasses.field()  # cached heuristic
    point: Point = dataclasses.field()
    time: int = dataclasses.field()

    # defining these for heapq usage
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, State) and self.h == other.h and self.time == other.time

    def __lt__(self, other: Any) -> bool:
        return isinstance(other, State) and self.time < other.time


def a_star_search(
    start: Point, target: Point, blizzards: set[Blizzard], width: int, height: int, start_time: int = 0
) -> list[State]:
    # TODO: could reuse `computed_blizzard_movements` between `a_star_search` calls. don't really feel like it atm tho.
    computed_blizzard_movements: dict[int, set[Point]] = {}  # where the blizzard will be at some time
    previous_points: dict[State, State] = {}

    def is_point_within_map(point: Point) -> bool:
        return (0 < point[0] < (width - 1) and 0 < point[1] < (height - 1)) or point in [start, target]

    def move_blizzard(point: Point, direction: int, time_steps: int) -> Point:
        # calculate how far the blizzard moves between t=0 and t=`time_steps`, then clamp it to the allowable board area
        new_point = add_points(point, apply_magnitude_to_point(DELTAS[direction], time_steps))
        clamped_point = ((new_point[0] - 1) % (width - 2) + 1), ((new_point[1] - 1) % (height - 2) + 1)
        return clamped_point

    def possible_moves(state: State) -> list[State]:
        new_time = state.time + 1
        if (blizzard_positions_at_time := computed_blizzard_movements.get(new_time, None)) is None:
            # blizzards have not yet been computed for this time step - compute and store them
            blizzard_positions_at_time = {
                move_blizzard(point=blizzard_point, direction=blizzard_direction, time_steps=new_time)
                for (blizzard_point, blizzard_direction) in blizzards
            }
            computed_blizzard_movements[new_time] = blizzard_positions_at_time

        return [
            State(point=p, time=new_time, h=heuristic(p, target))
            for p in [*[add_points(state.point, delta) for delta in DELTAS], state.point]
            if is_point_within_map(p) and p not in blizzard_positions_at_time
        ]

    def reconstruct_path(point: State) -> list[State]:
        if point in previous_points.keys():
            return [point] + reconstruct_path(previous_points[point])
        return [point]

    frontier: list[State] = []
    start_state = State(point=start, h=heuristic(start, target), time=start_time)
    heapq.heappush(frontier, start_state)
    g_score: dict[State, int] = {start_state: 0}
    while True:
        if not frontier:
            return []  # infeasible
        current_state = heapq.heappop(frontier)
        if current_state.point == target:
            return reconstruct_path(current_state)
        moves = possible_moves(current_state)
        for move in moves:
            tentative_score = g_score.get(current_state, 1_000_000) + (move.time - current_state.time)
            if tentative_score < g_score.get(move, 1_000_000):
                previous_points[move] = current_state
                g_score[move] = tentative_score
                heapq.heappush(frontier, move)


if __name__ == "__main__":
    t0 = time.time()
    s, e, b, w, h = read_input_file("input.txt")
    leg_1 = a_star_search(start=s, target=e, blizzards=b, width=w, height=h)
    if leg_1:
        print(f"Fastest time to reach the goal: {leg_1[0].time} mins.")
        leg_2 = a_star_search(start=e, target=s, blizzards=b, width=w, height=h, start_time=leg_1[0].time)
        assert len(leg_2) > 0
        leg_3 = a_star_search(start=s, target=e, blizzards=b, width=w, height=h, start_time=leg_2[0].time)
        assert len(leg_3) > 0
        print(f"Fastest time to reach the goal, then go back to the start and to the goal again: {leg_3[0].time} mins.")
    else:
        print("Problem is infeasible.")
    print(f"Solve completed in {round(time.time() - t0, 2)} seconds.")
