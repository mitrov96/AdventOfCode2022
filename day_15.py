def read_data():
    with open("input_day_15.txt") as f:
        data = f.read().splitlines()
        data = [line.split(" ") for line in data]
        res = []
        for line in data:
            sensor_x = int(line[2][2:-1])
            sensor_y = int(line[3][2:-1])
            beacon_x = int(line[8][2:-1])
            beacon_y = int(line[9][2:])
            res.append([(sensor_x, sensor_y), (beacon_x, beacon_y)])
    return res


def is_within_radius(start, radius, coordinate):
    distance = abs(start[0] - coordinate[0]) + abs(start[1] - coordinate[1])
    return distance <= radius


def set_grid(data, target_y=10):
    grid = set()
    sensors = set()
    beacons = set()
    for line in data:
        sensor, beacon = line
        sensors.add(sensor)
        beacons.add(beacon)

    for line in data:
        sensor, beacon = line
        radius = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        arm = radius - abs(sensor[1] - target_y)
        if arm <= 0:
            continue  # cannot reach target_y
        for x in range(sensor[0] - arm, sensor[0] + arm):
            grid.add(x)

    return grid


def compute_part2(data, max_xy):
    sensors = set()
    beacons = set()
    for line in data:
        sensor, beacon = line
        dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        sensors.add((sensor, dist))
        beacons.add(beacon)

    for line in data:
        sensor, beacon = line
        dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        top_most_y = sensor[1] + dist - 1
        bottom_most_y = sensor[1] - dist - 1
        for i in range(dist):
            for x, y in [
                (sensor[0] + i, top_most_y - i),
                (sensor[0] + i, bottom_most_y + i),
                (sensor[0] - i, top_most_y - i),
                (sensor[0] - i, bottom_most_y + i),
            ]:
                if x < 0 or x > max_xy or y < 0 or y > max_xy:
                    continue
                if (x, y) in beacons:
                    continue
                found = False
                for s2, s2_dist in sensors:
                    d = abs(s2[0] - x) + abs(s2[1] - y)
                    if d <= s2_dist:
                        found = True
                        break
                if not found:
                    return x * 4000000 + y


def main():
    data = read_data()
    # Part 1
    grid = set_grid(data, target_y=2000000)
    print("Part 1:", len(grid))
    # Part 2
    print("Part 2:", compute_part2(data, max_xy=4000000))


if __name__ == "__main__":
    main()
