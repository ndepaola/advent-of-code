from typing import TypeAlias

Point: TypeAlias = tuple[int, int]  # x, y
Transformation: TypeAlias = tuple[int, int]  # x delta, y delta


def get_transformations_with_magnitude(direction: str, magnitude_string: str) -> list[Transformation]:
    return [{"R": (1, 0), "U": (0, 1), "L": (-1, 0), "D": (0, -1)}[direction]] * int(magnitude_string)


def read_input_file(file_name: str = "input.txt") -> list[Transformation]:
    with open(file_name, "r") as f:
        return [
            transformation
            for line in f.readlines()
            for transformation in get_transformations_with_magnitude(*line.strip().split(" "))
        ]


def are_points_touching(point_a: Point, point_b: Point) -> bool:
    return point_b[0] - 1 <= point_a[0] <= point_b[0] + 1 and point_b[1] - 1 <= point_a[1] <= point_b[1] + 1


def clamp(number: int, min_: int = -1, max_: int = 1) -> int:  # clamp `number` to [`min_`, `max_`]
    return min(max(number, min_), max_)


def apply_transformation(point: Point, transformation: Transformation) -> Point:
    return point[0] + transformation[0], point[1] + transformation[1]


def apply_transformations(transformations: list[Transformation], num_knots: int) -> set[Point]:
    points_visited_by_tail: set[Point] = {(0, 0)}
    knots: list[Point] = [(0, 0)] * num_knots  # knots[0]: head, knots[-1]: tail
    for transformation in transformations:
        knots[0] = apply_transformation(knots[0], transformation)
        for i in range(1, num_knots):
            if are_points_touching(knots[i - 1], knots[i]):
                break  # all points in `knots` after this are guaranteed to also be touching - no need to check
            knot_transformation = clamp(knots[i - 1][0] - knots[i][0]), clamp(knots[i - 1][1] - knots[i][1])
            knots[i] = apply_transformation(knots[i], knot_transformation)  # follow the previous knot
        points_visited_by_tail.add(knots[-1])
    return points_visited_by_tail


if __name__ == "__main__":
    tf = read_input_file("input.txt")
    print(f"The tail of the 2-knot rope travelled to {len(apply_transformations(tf, num_knots=2))} points.")
    print(f"The tail of the 10-knot rope travelled to {len(apply_transformations(tf, num_knots=10))} points.")
