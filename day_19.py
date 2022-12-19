import sys
from pathlib import Path

file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

import re
from collections import deque
from tqdm import tqdm

with open('input_day_19.txt') as f:
    input_data = list(map(lambda x: x.replace('\n', ''), f.readlines()))


class Blueprint:
    def __init__(self, ore_cost, clay_cost, obsidian_cost, geode_cost):
        self.ore_cost = ore_cost
        self.clay_cost = clay_cost
        self.obsidian_cost = obsidian_cost
        self.geode_cost = geode_cost

    def __repr__(self) -> str:
        return str(self.__dict__)


blueprints = {}

pattern = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
for line in input_data:
    match = pattern.match(line)
    assert match is not None
    blueprint_id, ore_cost, clay_cost, robot_cost_ore, robot_cost_clay, geode_cost_ore, geode_cost_obsidian = map(int,
                                                                                                                  match.groups())
    # dprint(blueprint_id, ore_cost, clay_cost, robot_cost_ore, robot_cost_clay, geode_cost_ore, geode_cost_obsidian)
    blueprints[blueprint_id] = Blueprint(ore_cost, clay_cost, (robot_cost_ore, robot_cost_clay),
                                         (geode_cost_ore, geode_cost_obsidian))

robot_names = ["Ore", "Clay", "Obsidian", "Geode"]


def clamp(number, max):
    return max if number >= max else number


def get_max_geodes(blueprint, time):
    ore_cost, clay_cost, (obsidian_cost_ore, obsidian_cost_clay), (geode_cost_ore,
                                                                   geode_cost_obsidian) = blueprint.ore_cost, blueprint.clay_cost, blueprint.obsidian_cost, blueprint.geode_cost
    best = 0
    initial_state = (0, 0, 0, 0, 1, 0, 0, 0, time)
    queue = deque([initial_state])
    seen = set()
    while queue:
        ore, clay, obsidian, geodes, ore_bots, clay_bots, obsidian_bots, geode_bots, time = queue.popleft()
        best = max(best, geodes)
        if time == 0:
            continue

        max_ore = max([ore_cost, clay_cost, obsidian_cost_ore, geode_cost_ore])  # The max ore that we would ever want

        # Discard extra bots
        ore_bots = clamp(ore_bots, max_ore)
        clay_bots = clamp(clay_bots, obsidian_cost_clay)
        obsidian_bots = clamp(obsidian_bots, geode_cost_obsidian)

        # Discard extra ore
        ore = clamp(ore, time * max_ore - ore_bots * (time - 1))
        clay = clamp(clay, time * obsidian_cost_clay - clay_bots * (time - 1))
        obsidian = clamp(obsidian, time * geode_cost_obsidian - obsidian_bots * (time - 1))

        state = (ore, clay, obsidian, geodes, ore_bots, clay_bots, obsidian_bots, geode_bots, time)

        if state in seen:
            continue
        seen.add(state)

        if len(queue) % 10000 == 0:
            print(f"Left: {time} - {len(queue)}", end="\r")

        # === Consider all possible scenarios ===

        # Do nothing
        queue.append((ore + ore_bots, clay + clay_bots, obsidian + obsidian_bots, geodes + geode_bots, ore_bots,
                      clay_bots, obsidian_bots, geode_bots, time - 1))

        if ore >= ore_cost:  # Buy an ore bot
            queue.append((ore - ore_cost + ore_bots, clay + clay_bots, obsidian + obsidian_bots, geodes + geode_bots,
                          ore_bots + 1, clay_bots, obsidian_bots, geode_bots, time - 1))

        if ore >= clay_cost:  # Buy a clay bot
            queue.append((ore - clay_cost + ore_bots, clay + clay_bots, obsidian + obsidian_bots, geodes + geode_bots,
                          ore_bots, clay_bots + 1, obsidian_bots, geode_bots, time - 1))

        if ore >= obsidian_cost_ore and clay >= obsidian_cost_clay:  # Buy an obsidian bot
            queue.append((ore - obsidian_cost_ore + ore_bots, clay - obsidian_cost_clay + clay_bots,
                          obsidian + obsidian_bots, geodes + geode_bots, ore_bots, clay_bots, obsidian_bots + 1,
                          geode_bots, time - 1))

        if ore >= geode_cost_ore and obsidian >= geode_cost_obsidian:  # Buy a geode bot
            queue.append((ore - geode_cost_ore + ore_bots, clay + clay_bots,
                          obsidian - geode_cost_obsidian + obsidian_bots, geodes + geode_bots, ore_bots, clay_bots,
                          obsidian_bots, geode_bots + 1, time - 1))
    print()
    return best


def part_1():
    qualities = 0
    for blueprint_id, blueprint in tqdm(blueprints.items()):
        geodes = get_max_geodes(blueprint, 24)
        quality = geodes * blueprint_id
        qualities += quality
    return qualities


def part_2():
    value = 1
    for i in range(1, min(4, len(blueprints) + 1)):
        print(f"Calculating blueprint {i}")
        value *= get_max_geodes(blueprints[i], 32)
    return value


print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")
