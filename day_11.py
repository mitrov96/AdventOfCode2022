import math


class Monkey:
    def __init__(self, idx, s):
        self.idx = idx
        self.inv = list(map(int, map(str.strip, s[1].replace('Starting items: ', '').split(','))))
        self.op = s[2].replace('Operation: ', '').replace('new = ', '')
        self.div = int(s[3].replace('Test: divisible by ', ''))
        self.tr = int(s[4].replace('If true: throw to monkey ', ''))
        self.fa = int(s[5].replace('If false: throw to monkey ', ''))
        self.inspections = 0

    def add_item(self, item):
        self.inv.append(item)

    def inspects(self):
        self.inspections += 1
        return self.inv.pop(0)

    def __repr__(self):
        s_inv = ", ".join(map(str, self.inv))
        return f"Monkey {self.idx}: {s_inv}"


if __name__ == "__main__":
    monkeys = {}
    with open('input_day_11.txt') as fin:
        inp = [e.strip() for e in fin.readlines()]
        for midx in range((len(inp) + 1) // 7):
            monkeys[midx] = Monkey(midx, inp[7 * midx:(7 * (midx + 1) - 1)])
        for rnd in range(20):
            for midx in sorted(monkeys.keys()):
                m = monkeys[midx]
                while m.inv:
                    item = m.inspects()
                    _op = str(m.op).replace('old', str(item))
                    worry = math.floor(eval(_op) / 3.0)
                    if worry % m.div == 0:
                        monkeys[m.tr].add_item(worry)
                    else:
                        monkeys[m.fa].add_item(worry)
    std = sorted([m.inspections for m in monkeys.values()])
    print(std[-1] * std[-2])
