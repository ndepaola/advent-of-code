from typing import TypeAlias

Point: TypeAlias = tuple[int, int, int]  # x, y, z


def read_input_file(file_name: str = "input.txt") -> set[Point]:
    with open(file_name, "r") as f:
        return {tuple(map(lambda x: int(x), line.strip().split(","))) for line in f.readlines() if line.strip()}  # type: ignore


def get_adjacencies(point: Point) -> set[Point]:
    return {
        (point[0] + 1, point[1], point[2]),
        (point[0] - 1, point[1], point[2]),
        (point[0], point[1] + 1, point[2]),
        (point[0], point[1] - 1, point[2]),
        (point[0], point[1], point[2] + 1),
        (point[0], point[1], point[2] - 1),
    }


def compute_total_surface_area(points: set[Point]) -> int:
    return sum([6 - len(points & get_adjacencies(point)) for point in points])


def compute_exterior_surface_area(points: set[Point]) -> int:
    # determine the bounding rectangular prism of the sphere
    min_x, max_x, min_y, max_y, min_z, max_z = 0, 0, 0, 0, 0, 0
    for point in points:
        min_x, max_x = min(min_x, point[0]), max(max_x, point[0])
        min_y, max_y = min(min_y, point[1]), max(max_y, point[1])
        min_z, max_z = min(min_z, point[2]), max(max_z, point[2])

    outside_points = set()  # use flood fill to identify all points outside the sphere
    q: list[Point] = [  # attempt to fill from each corner of the bounding prism
        (min_x, min_y, min_z),
        (max_x, max_y, min_z),
        (max_x, min_y, min_z),
        (min_x, max_y, min_z),
        (min_x, min_y, max_z),
        (max_x, max_y, max_z),
        (max_x, min_y, max_z),
        (min_x, max_y, max_z),
    ]
    while q:
        p_ = q.pop()
        if not (min_x <= p_[0] <= max_x and min_y <= p_[1] <= max_y and min_z <= p_[2] <= max_z) or p_ in points:
            continue
        outside_points.add(p_)
        for p__ in [
            (p_[0] + 1, p_[1], p_[2]),
            (p_[0] - 1, p_[1], p_[2]),
            (p_[0], p_[1] + 1, p_[2]),
            (p_[0], p_[1] - 1, p_[2]),
            (p_[0], p_[1], p_[2] + 1),
            (p_[0], p_[1], p_[2] - 1),
        ]:
            if p__ not in outside_points:
                q.append(p__)

    return compute_total_surface_area(  # all points in the prism - outside points => all points in the sphere
        {
            (x_value, y_value, z_value)
            for x_value in range(min_x, max_x + 1)
            for y_value in range(min_y, max_y + 1)
            for z_value in range(min_z, max_z + 1)
        }
        - outside_points
    )


if __name__ == "__main__":
    p = read_input_file("input.txt")
    print(f"The total surface area of the lava droplet (including the interior) is {compute_total_surface_area(p)}.")
    print(f"The total surface area of the lava droplet (excluding the interior) is {compute_exterior_surface_area(p)}.")
