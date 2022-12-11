with open('input_day_10.txt') as f:
    lines = f.readlines()

operations = []
cycle = 1
values = []
x = 1

cycles_to_find = [20, 60, 100, 140, 180, 220]

total = 0

for line in lines:
    if line.strip() == 'noop':
        operations.append('noop')
    elif line.strip().split()[0] == 'addx':
        operations.append('noop')
        operations.append(line)

for op in operations:
    # DURING CYCLE
    if cycle in cycles_to_find:
        values.append(x)
    # AFTER CYCLE
    cycle = cycle + 1
    if op == 'noop':
        continue
    elif op.split()[0] == 'addx':
        x = x + int(op.split()[1])

for i in range(len(values)):
    total = total + (values[i] * cycles_to_find[i])

print(total)
