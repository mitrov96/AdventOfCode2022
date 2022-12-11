from functools import reduce

from day_11 import Monkey

if __name__ == "__main__":
    monkeys = {}
    with open('input_day_11.txt') as fin:
        inp = [e.strip() for e in fin.readlines()]
        for midx in range((len(inp) + 1) // 7):
            monkeys[midx] = Monkey(midx, inp[7 * midx:(7 * (midx + 1) - 1)])
        lcm = reduce((lambda a, b: a * b), [m.div for m in monkeys.values()])
        for rnd in range(10000):
            for midx in sorted(monkeys.keys()):
                m = monkeys[midx]
                while m.inv:
                    item = m.inspects()
                    _op = str(m.op).replace('old', str(item))
                    worry = eval(_op) % lcm
                    if worry % m.div == 0:
                        monkeys[m.tr].add_item(worry)
                    else:
                        monkeys[m.fa].add_item(worry)
    std = sorted([m.inspections for m in monkeys.values()])
    print(std[-1] * std[-2])
