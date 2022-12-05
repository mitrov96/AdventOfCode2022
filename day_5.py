with open("input_day_5.txt", "r") as f:
    input = f.read()

stack = [[] for i in range(9)]
stack2 = [[] for i in range(9)]

matrix = input.split('\n\n')[0].replace('[', '').replace(']', '').replace('    ', ' ')
moves = [a.split(',') for a in
         input.strip().split('\n\n')[1].replace('move ', '').replace(' from ', ',').replace(' to ', ',').split('\n')]

arr = [b.split(' ') for b in matrix.split('\n')][:-1]

for a in arr[::-1]:
    for idx, b in enumerate(a):
        if b != '':
            stack[idx].append(b)
            stack2[idx].append(b)

for move in moves:
    sk2 = []
    for i in range(int(move[0])):
        a = stack[int(move[1]) - 1].pop()
        sk2.append(stack2[int(move[1]) - 1].pop())
        stack[int(move[2]) - 1].append(a)
    while sk2 != []:
        stack2[int(move[2]) - 1].append(sk2.pop())

part_one = "".join([a[-1] if len(a) > 0 else '' for a in stack])
part_two = "".join([a[-1] if len(a) > 0 else '' for a in stack2])
print("Part one: %s" % part_one)
print("Part two: %s" % part_two)
