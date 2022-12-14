with open("input_day_14.txt", "r") as f:
    lines = [line.strip() for line in f.readlines()]

rock_set = set()
for line in lines:
    L = [list(map(int, coord.split(","))) for coord in line.split(" -> ")]
    for i in range(len(L) - 1):
        x1, y1 = L[i]
        x2, y2 = L[i + 1]
        rock_set = rock_set.union(
            {
                (x, y)
                for x in range(min(x1, x2), max(x1, x2) + 1)
                for y in range(min(y1, y2), max(y1, y2) + 1)
            }
        )

dead = max(y for _, y in rock_set) + 1


def drop_sand(time: int = 0) -> int:
    sand_pos = (500, 0)
    while True:
        x, y = sand_pos
        if y >= dead:
            return -1
        elif (x, y + 1) not in rock_set:
            sand_pos = (x, y + 1)
            continue
        elif (x - 1, y + 1) not in rock_set:
            sand_pos = (x - 1, y + 1)
            continue
        elif (x + 1, y + 1) not in rock_set:
            sand_pos = (x + 1, y + 1)
            continue
        rock_set.add(sand_pos)
        time += 1
        break
    return time


if __name__ == "__main__":
    counter = 0
    while (time := drop_sand(counter)) != -1:
        counter = time
    print(counter)
