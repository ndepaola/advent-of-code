import re
import time
from itertools import chain
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
    sensors = set(sensor_map.keys())
    all_points_where_beacons_could_go: set[Point] = {
        man
        for sensor, sensor_dist in sensor_map.items()
        for man in [
            (x_, y)
            for x_ in range(
                max(sensor[0] - (sensor_map[sensor] - abs(y - sensor[1])), dimensions[0][0]),
                min(sensor[0] + (sensor_map[sensor] - abs(y - sensor[1])) + 1, dimensions[0][1])
            )
            if (x_, y) not in beacons and (x_, y) not in sensors
        ]
    }
    return len(all_points_where_beacons_could_go)


def get_beacon_edges(p: Point, d: int) -> Iterable[Point]:
    return zip(
        chain(range(p[0] - d, p[0] + d), range(p[0] + d, p[0] - d, -1)),
        chain(range(p[1], p[1] + d), range(p[1] + d, p[1] - d, -1), range(p[1] - d, p[1])),
    )


def point_is_within_range_of_a_beacon(p: Point, s: SensorMap) -> bool:
    for point, distance in s.items():
        if manhattan_distance(p, point) <= distance:
            return True
    return False


def find_distress_signal(file_name: str, min_x: int, max_x: int, min_y: int, max_y: int) -> Point | None:
    def is_point_within_map(point_: Point) -> bool:
        return min_x <= point_[0] <= max_x and min_y <= point_[1] <= max_y

    sensor_map, beacons, dimensions = read_input_file(file_name=file_name)
    for i, point in enumerate(sensor_map.keys()):
        edge_points = get_beacon_edges(point, sensor_map[point] + 1)
        for edge_point in edge_points:
            if is_point_within_map(edge_point) and not point_is_within_range_of_a_beacon(edge_point, sensor_map):
                return edge_point
    return None


if __name__ == "__main__":
    t0 = time.time()
    print(
        f"There are {count_possible_distress_signal_positions_at_y_level(file_name='input.txt', y=2_000_000)} "
        f"places where the distress signal could be coming from at y=2,000,000. "
        f"Computing this took {round(time.time() - t0, 2)} seconds."
    )
    t1 = time.time()
    s = find_distress_signal(file_name="input.txt", min_x=0, max_x=4000000, min_y=0, max_y=4000000)
    if s is not None:
        freq = s[0] * 4000000 + s[1]
        print(f"The location of the distress signal is {s} and its tuning frequency is {freq}. ", end="")
    else:
        print("The distress signal could not be found. ", end="")
    print(f"Computing this took {round(time.time() - t1, 2)} seconds.")
