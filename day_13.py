import re


class PacketPair:
    def __init__(self, packet_1, packet_2):
        self.packet_1 = packet_1
        self.packet_2 = packet_2

    def is_ordered(self):
        return self.compare(self.packet_1, self.packet_2)

    def compare(self, left, right, level=0):
        if type(left) == int and type(right) == int:
            if left != right:
                return left < right
            else:
                return None
        elif type(left) == list and type(right) == list:
            i = 0
            while i < len(left) and i < len(right):
                result = self.compare(left[i], right[i], level + 1)
                if result is None:
                    i += 1
                else:
                    return result
            if len(left) == len(right):
                return None
            else:
                return len(left) < len(right)
        elif type(left) == int and type(right) == list:
            return self.compare([left], right, level + 1)
        elif type(left) == list and type(right) == int:
            return self.compare(left, [right], level + 1)
        else:
            raise Exception(f"Unknown types: {type(left)} and {type(right)}")

    def __str__(self):
        return f"PacketPair({self.packet_1}, {self.packet_2})"

    def __repr__(self):
        return self.__str__()


def main():
    with open("input_day_13.txt", "r") as input_file:
        input = input_file.read().strip()
    print(sum_inorder_packets(read_packets(input)))


def read_packets(input):
    pairs = []
    input_list = input.split("\n\n")
    for input_pair in input_list:
        packet_1, packet_2 = input_pair.split("\n")
        pairs.append(PacketPair(read_packet(packet_1), read_packet(packet_2)))
    return pairs


def read_packet(packet_string):
    stack = []
    for char in [x for x in re.split("(\d+|\D)", packet_string) if x != ""]:
        if char == "[":
            stack.append([])
        elif char == "]":
            if len(stack) > 1:
                stack[-2].append(stack.pop())
        elif char == ",":
            pass
        else:
            stack[-1].append(int(char))
    return stack[0]


def sum_inorder_packets(packets):
    sum = 0
    for i in range(len(packets)):
        if packets[i].is_ordered():
            sum += i + 1
    return sum


if __name__ == "__main__":
    main()
