with open('input_day_10.txt') as f:
    lines = f.readlines()

operations = []
cycle = 0
values = []
x = 1

cycles_to_find = [40, 80, 120, 160, 200, 240]

for line in lines:
    if line.strip() == 'noop':
        operations.append('noop')
    elif line.strip().split()[0] == 'addx':
        operations.append('noop')
        operations.append(line)

for op in operations:
    if cycle in list(range(x - 1, x + 2)):
        values.append('#')
    else:
        values.append(".")
    cycle = cycle + 1
    if op == 'noop':
        None
    elif op.split()[0] == 'addx':
        x = x + int(op.split()[1])

    if cycle == 40:
        cycle = 0

for i in range(1, len(operations) + 1):
    print(values[i - 1], end='')
    if i in cycles_to_find:
        print()
