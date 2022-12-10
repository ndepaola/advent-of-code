from typing import Iterable, TypeAlias

Pair: TypeAlias = tuple[int, int]
TreeGrid: TypeAlias = dict[Pair, int]


def read_input_file(file_name: str = "input.txt") -> TreeGrid:
    with open(file_name, "r") as f:
        return {(r, c): int(height) for r, line in enumerate(f.readlines()) for c, height in enumerate(line.strip())}


def get_slices(pair: Pair, h: int, w: int) -> Iterable[Iterable[Pair]]:
    yield ((x, pair[1]) for x in reversed(range(0, pair[0])))  # up
    yield ((x, pair[1]) for x in range(pair[0] + 1, h))  # down
    yield ((pair[0], x) for x in reversed(range(0, pair[1])))  # left
    yield ((pair[0], x) for x in range(pair[1] + 1, w))  # right


def check_tree(grid: TreeGrid, pair: Pair, h: int, w: int) -> tuple[bool, int]:
    total_score = 1
    tree_is_visible = False
    for grid_slice in get_slices(pair, h, w):
        slice_score = 0
        checked_entirety_of_slice = True
        for slice_pair in grid_slice:
            slice_score += 1
            if grid[slice_pair] >= grid[pair]:
                checked_entirety_of_slice = False
                break
        tree_is_visible = tree_is_visible or checked_entirety_of_slice
        total_score *= slice_score
    return tree_is_visible, total_score


if __name__ == "__main__":
    tree_grid = read_input_file("input.txt")
    h, w = [max(x) + 1 for x in zip(*tree_grid.keys())]  # calculate height and width of forest
    trees_visible, scenic_scores = zip(
        *[check_tree(grid=tree_grid, pair=(r, c), h=h, w=w) for r in range(1, h - 1) for c in range(1, w - 1)]
    )
    print(f"The number of partially visible trees in the forest is {(h * 2 + w * 2 - 4) + sum(trees_visible)}.")
    print(f"The maximum scenic score in the forest is {max(scenic_scores)}.")
