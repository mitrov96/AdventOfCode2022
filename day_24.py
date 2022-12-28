import math
from functools import lru_cache


def lcm(a, b):
    return a * b // math.gcd(a, b)


def move_in_dir(pos, dir):
    return (pos[0] + dir[0], pos[1] + dir[1])


class Blizzards(object):
    def __init__(self, starting_positions_and_dirs, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.max_period = lcm(size_x, size_y)
        self.positions_to_times = {}
        blizzards = starting_positions_and_dirs[:]

        for time in range(self.max_period):
            # Record each blizzard position
            for (blizzard_pos, _blizzard_dir) in blizzards:
                if blizzard_pos not in self.positions_to_times:
                    self.positions_to_times[blizzard_pos] = set()
                self.positions_to_times[blizzard_pos].add(time)

            # Move each blizzard
            for i in range(len(blizzards)):
                (blizzard_pos, blizzard_dir) = blizzards[i]
                blizzard_pos = move_in_dir(blizzard_pos, blizzard_dir)
                blizzard_pos = (blizzard_pos[0] % self.size_x, blizzard_pos[1] % self.size_y)
                blizzards[i] = (blizzard_pos, blizzard_dir)

    def blizzard_exists_at_time(self, position, time) -> bool:
        time %= self.max_period
        if position not in self.positions_to_times:
            return False
        return time in self.positions_to_times[position]


lines = open("input_day_24.txt").read().strip().split("\n")
blizzards = []

assert lines[0].startswith("#.")
assert lines[-1].endswith(".#")

lines = lines[1:-1]
size_x = len(lines)
size_y = len(lines[0]) - 2
for i, line in enumerate(lines):
    assert line.startswith("#")
    assert line.endswith("#")
    line = line[1:-1]
    for j, c in enumerate(line):
        blizzard_pos = (i, j)
        if c == ".":
            continue
        if c == "<":
            blizzard_dir = (0, -1)
        elif c == ">":
            blizzard_dir = (0, 1)
        elif c == "^":
            blizzard_dir = (-1, 0)
        elif c == "v":
            blizzard_dir = (1, 0)
        else:
            assert False
        blizzards.append((blizzard_pos, blizzard_dir))
blizzards = Blizzards(blizzards, size_x, size_y)
max_period = lcm(size_x, size_y)


# Part 1
# We can represent this as a BFS on a graph of (position * time modulo max_period), and the earliest time we reach there
@lru_cache(maxsize=None)
def possible_next_vertex(vertex, size_x, size_y):
    if vertex == "start":
        return ["start", (0, 0)]
    if vertex == "end":
        return ["end", (size_x - 1, size_y - 1)]

    (x, y) = vertex
    neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    neighbours = [(x, y) for (x, y) in neighbours if x >= 0 and x < size_x and y >= 0 and y < size_y]

    if (x, y) == (size_x - 1, size_y - 1):
        neighbours.append("end")  # type: ignore
    if (x, y) == (0, 0):
        neighbours.append("start")  # type: ignore

    # We can also choose to wait where we are.
    neighbours.append((x, y))
    return neighbours


# Keys are (vertex, modulus of time when we were there)
def times_to_end(start_vertex, end_vertex, start_time):
    time = start_time
    earliest_visited_time = {(start_vertex, time % max_period): time}
    frontier = [start_vertex]
    dictionary_entries_for_end_vertex = 0

    while frontier:
        if len(earliest_visited_time) % 10_000 == 0:
            print(len(earliest_visited_time))
        time += 1
        new_frontier_set = set()

        for v1 in frontier:
            for v2 in possible_next_vertex(v1, size_x, size_y):
                if v2 in new_frontier_set: continue
                if (v2, time % max_period) in earliest_visited_time:
                    continue

                if v2 != "end" and v2 != "start":
                    if blizzards.blizzard_exists_at_time(v2, time):
                        continue

                earliest_visited_time[(v2, time % max_period)] = time
                new_frontier_set.add(v2)
                if v2 == end_vertex:
                    return time
        frontier = list(new_frontier_set)
    assert False


t1 = times_to_end("start", "end", 0)
print(t1)
t2 = times_to_end("end", "start", t1)
print(t2)
t3 = times_to_end("start", "end", t2)
print(t3)
