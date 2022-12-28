def parse_input(inp):
    elves = set()

    for i, row in enumerate(inp):
        for j, col in enumerate(row):
            if col == '#': elves.add(Elf(j - 1j * i))

    return elves


class Elf(complex):
    adjacent = (1, 1 - 1j, 1 + 1j, -1, -1 - 1j, -1 + 1j, 1j, -1j)

    check = {1j: (1j - 1, 1j, 1j + 1),
             -1j: (-1j - 1, -1j, -1j + 1),
             1: (1 - 1j, 1, 1 + 1j),
             -1: (-1 - 1j, -1, -1 + 1j)}

    def am_alone(self, others):

        return not {self + i for i in self.adjacent} & others

    def next_move(self, others, order):

        for move in order:
            if not {self + i for i in self.check[move]} & others:
                return Elf(self + move)

        return self

    def propose(self, others, order):

        if self.am_alone(others):
            return self
        else:
            return self.next_move(others, order)


def simulate(elves, n):
    order = (1j, -1j, -1, 1)
    rnd = 0

    while rnd < n:
        changed = False
        proposals = dict()
        counts = dict()
        for elf in elves:
            prop = elf.propose(elves, order)
            proposals[elf] = prop
            counts[prop] = counts.get(prop, 0) + 1
        for elf, move in proposals.items():
            if counts[move] == 1 and elf != move:
                changed = True
                elves.remove(elf)
                elves.add(move)
        order = order[1:] + order[:1]
        rnd += 1

        if not changed: break

    return rnd, elves


def sol_1(elves):
    rnd, elves = simulate(elves.copy(), 10)

    real = [int(elf.real) for elf in elves]
    imag = [int(elf.imag) for elf in elves]

    return (max(real) - min(real) + 1) * (max(imag) - min(imag) + 1) - len(elves)


def sol_2(elves):
    rnd, elves = simulate(elves.copy(), float('inf'))

    return rnd


if __name__ == '__main__':
    with open('input_day_23.txt') as inp:
        raw = inp.read().splitlines()
        elves = parse_input(raw)
        solution1 = sol_1(elves)
        print(solution1)
        solution2 = sol_2(elves)
        print(solution2)
