input = open('input_day_6.txt').read()


def pack_marker(marker_value):
    for i in range(len(input)):
        set_char = input[i:i + marker_value]
        if len(set(set_char)) == len(set_char):
            a = input.rindex(set_char) + marker_value
            break
    return a


print(pack_marker(4))
print(pack_marker(14))
