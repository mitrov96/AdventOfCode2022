import functools


def compare(left, right):
    in_order = 0
    for index in range(min(len(left), len(right))):
        if type(left[index]) == int and type(right[index]) == list:
            left[index] = [left[index]]
        if type(right[index]) == int and type(left[index]) == list:
            right[index] = [right[index]]
        if type(left[index]) == int and type(right[index]) == int:
            if left[index] > right[index]:
                return -1
            if left[index] < right[index]:
                return 1
        if type(left[index]) == list and type(right[index]) == list:
            result = compare(left[index], right[index])
            if result != 0:
                return result
    if in_order == 0:
        if len(left) < len(right):
            return 1
        if len(right) < len(left):
            return -1
    return in_order


input = open("input_day_13.txt").read().split('\n\n')
lines = [[[2]], [[6]]]
for pair_index, pair in enumerate(input):
    lines += map(eval, pair.split('\n')[0:2])
lines = sorted(lines, key=functools.cmp_to_key(compare), reverse=True)
indexes = [i + 1 for i, line in enumerate(lines) if line == [[[[2]]]] or line == [[[[6]]]]]
print(indexes[0] * indexes[1])
