import time
from collections import defaultdict
from typing import TypeAlias

Point: TypeAlias = tuple[int, int]  # x, y. top-left is 0, 0.


def read_input_file(file_name: str = "input.txt") -> set[Point]:
    with open(file_name, "r") as f:
        return {(x, y) for y, line in enumerate(f.readlines()) for x, ch in enumerate(line.strip()) if ch == "#"}


def add_points(point_a: Point, point_b: Point) -> Point:
    return point_a[0] + point_b[0], point_a[1] + point_b[1]


def get_all_neighbours_for_point(point: Point) -> set[Point]:
    return {  # hard-coding these is actually much faster than iterating over the 3x3 area and excluding `point`
        (point[0] - 1, point[1] + 1),
        (point[0], point[1] + 1),
        (point[0] + 1, point[1] + 1),
        (point[0] - 1, point[1]),
        (point[0] + 1, point[1]),
        (point[0] - 1, point[1] - 1),
        (point[0], point[1] - 1),
        (point[0] + 1, point[1] - 1),
    }


def simulate_elf_movements(elves: set[Point], num_rounds: int | None) -> tuple[int, set[Point]]:
    mutated_elves = {*elves}
    deltas = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # north, south, west, east
    proposed_direction: int = 0
    n: int = 0
    while True:
        # first half of the round - elves propose where to move
        proposals: dict[Point, list[Point]] = defaultdict(list)  # point => the elves proposing to move to that point
        for elf in mutated_elves:
            # if none of the neighbours of this elf are occupied, do not move the elf
            if not (get_all_neighbours_for_point(elf) & mutated_elves):
                continue
            for delta_index in range(len(deltas)):
                delta = deltas[(delta_index + proposed_direction) % len(deltas)]
                elf_plus_delta = add_points(elf, delta)
                man = [i for i, x in enumerate(delta) if x != 0].pop()
                neighbours = {x for x in get_all_neighbours_for_point(elf) if elf_plus_delta[man] == x[man]}
                if not (mutated_elves & neighbours):
                    # no elves occupy this space - propose moving here
                    proposals[elf_plus_delta].append(elf)
                    break

        # second half of the round - elves move according to their proposals if nobody else proposed the same thing
        if not proposals:
            break  # no elves are moving this round - terminate the simulation here
        for proposed_position, elves_proposing_position in proposals.items():
            if len(elves_proposing_position) == 1:
                elf_proposing_direction = elves_proposing_position.pop()
                mutated_elves.remove(elf_proposing_direction)
                mutated_elves.add(proposed_position)

        # end of round bookkeeping
        proposed_direction += 1
        n += 1
        if num_rounds is not None and n >= num_rounds:
            break
    return n, mutated_elves


def calculate_empty_ground_tiles(elves: set[Point]) -> int:
    all_x, all_y = list(zip(*elves))
    min_x, max_x, min_y, max_y = min(all_x), max(all_x), min(all_y), max(all_y)
    return len({(x, y) for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1) if (x, y) not in elves})


if __name__ == "__main__":
    e = read_input_file("input.txt")
    t0 = time.time()
    print(
        "The number of empty ground tiles in the bounding rectangle after 10 rounds of Elf movements is "
        f"{calculate_empty_ground_tiles(simulate_elf_movements(e, num_rounds=10)[1])}."
    )
    print(f"The first round where no Elves move is round {simulate_elf_movements(e, num_rounds=None)[0]+1}.")
    print(f"Both simulations took {round(time.time() - t0, 2)} seconds to run (in total).")
