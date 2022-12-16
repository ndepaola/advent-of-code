import re
import time
from typing import Iterable, TypeAlias

Point: TypeAlias = tuple[int, int]  # x, y, distance to closest beacon
SensorMap: TypeAlias = dict[Point, int]  # (x, y) => distance to closest beacon
Dimensions = tuple[Point, Point]  # (min x, min y), (max x, max y)


def manhattan_distance(point_a: Point, point_b: Point) -> int:
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


def read_input_file(file_name: str = "input.txt") -> tuple[SensorMap, set[Point], Dimensions]:
    sensor_map: SensorMap = {}
    beacons: set[Point] = set()
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    with open(file_name, "r") as f:
        for line in f.readlines():
            if stripped_line := line.strip():
                sensor_x, sensor_y, beacon_x, beacon_y = [
                    int(x)
                    for x in re.match(
                        r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$", stripped_line
                    ).groups()  # type: ignore  # technically sloppy but known input data so w/e
                ]
                dist = manhattan_distance((sensor_x, sensor_y), (beacon_x, beacon_y))
                sensor_map[(sensor_x, sensor_y)] = dist
                beacons.add((beacon_x, beacon_y))
                min_x, min_y = min(min_x, sensor_x, beacon_x - dist), min(min_y, sensor_y, beacon_y - dist)
                max_x, max_y = max(max_x, sensor_x, beacon_x + dist), max(max_y, sensor_y, beacon_y + dist)
    return sensor_map, beacons, ((min_x, max_x), (min_y, max_y))


def count_possible_distress_signal_positions_at_y_level(file_name: str = "input.txt", y: int = 2_000_000) -> int:
    sensor_map, beacons, dimensions = read_input_file(file_name=file_name)
    all_points_where_beacons_could_go: set[Point] = set()
    for i, point in enumerate(sensor_map.keys()):
        t0 = time.time()
        for x in range(dimensions[0][0], dimensions[0][1] + 1):  # attempt to speed up with short circuit eval
            if abs(y - point[1]) <= sensor_map[point] and manhattan_distance((x, y), point) <= sensor_map[point]:
                all_points_where_beacons_could_go.add((x, y))
        print(f"Checking point {i} took about {round(time.time() - t0, 2)} seconds.")
    return len((all_points_where_beacons_could_go - beacons) - set(sensor_map.keys()))


def get_point_neighbours_within_map(p: Point, min_x: int, max_x: int, min_y: int, max_y: int) -> Iterable[Point]:
    def is_point_within_map(point_: Point) -> bool:
        return min_x <= point_[0] <= max_x and min_y <= point_[1] <= max_y

    for point in (p, (p[0] - 1, p[1]), (p[0] + 1, p[1]), (p[0], p[1] - 1), (p[0], p[1] + 1), *get_beacon_edges(p, 2)):
        if is_point_within_map(point):
            yield point


def get_beacon_edges(p: Point, d: int) -> list[Point]:
    return list(
        zip(
            list(range(p[0] - d, p[0] + d)) + list(range(p[0] + d, p[0] - d, -1)),
            list(range(p[0], p[0] + d)) + list(range(p[0] + d, p[0] - d, -1)) + list(range(p[0] - d, p[0])),
        )
    )


def point_is_within_range_of_a_beacon(p: Point, s: SensorMap) -> bool:
    for point, distance in s.items():
        if manhattan_distance(p, point) <= distance:
            return True
    return False


def find_distress_signal(file_name: str, min_x: int, max_x: int, min_y: int, max_y: int) -> Point | None:
    sensor_map, beacons, dimensions = read_input_file(file_name=file_name)
    for i, point in enumerate(sensor_map.keys()):
        t0 = time.time()
        edge_points = get_beacon_edges(point, sensor_map[point])
        for edge_point in edge_points:
            for edge_point_neighbour in get_point_neighbours_within_map(
                edge_point, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y
            ):
                if not point_is_within_range_of_a_beacon(edge_point_neighbour, sensor_map):
                    return edge_point_neighbour
        print(f"Checking point {i} took about {round(time.time() - t0, 2)} seconds.")
    return None


if __name__ == "__main__":
    # print(
    #     f"There are {count_possible_distress_signal_positions_at_y_level(file_name='input.txt', y=2_000_000)} "
    #     f"places where the distress signal could be coming from at y=10."
    # )
    # a = find_distress_signal(file_name="example.txt", min_x=0, max_x=20, min_y=0, max_y=20)
    a = find_distress_signal(file_name="input.txt", min_x=0, max_x=4000000, min_y=0, max_y=4000000)
    if a is None:
        print("no solution found :(")
    else:
        print(a[0] * 4000000 + a[1])
        print(a)
