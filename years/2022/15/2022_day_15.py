import re
import time
from typing import TypeAlias

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


if __name__ == "__main__":
    print(
        f"There are {count_possible_distress_signal_positions_at_y_level(file_name='input.txt', y=2_000_000)} "
        f"places where the distress signal could be coming from at y=10."
    )

    # TODO: let this run for ages
    sensor_map, beacons, dimensions = read_input_file(file_name="input.txt")
    for x in range(0, 2000000 + 1):
        for y in range(0, 2000000 + 1):
            within_sight = False
            for point in sensor_map.keys():
                if manhattan_distance((x, y), point) <= sensor_map[point]:
                    within_sight = True
                    break
            if not within_sight:
                print(f"Hurrah we did it at {(x*4000000+y)}")
