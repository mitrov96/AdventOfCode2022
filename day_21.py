class node:
    all_nodes = {}
    parents = {}

    def __init__(self, name, value, left, right, operator) -> None:
        self.name: str = name
        self.value: int = value
        self.left: function = lambda: node.all_nodes[left]
        self.right: function = lambda: node.all_nodes[right]
        self.operator: str = operator

        node.all_nodes[name] = self
        if left is not None:
            node.parents[left] = self
        if right is not None:
            node.parents[right] = self

    def get_value(self):
        if self.value is not None:
            return self.value
        return eval("self.left().get_value()" + self.operator + "self.right().get_value()")

    def get_steps(self):
        current = self
        steps = []
        while current.name != "root":
            parent = node.parents[current.name]
            if parent.left() == current:
                steps.append("left")
            if parent.right() == current:
                steps.append("right")
            current = parent
        return steps[::-1]

    def get_child(self, direction):
        if direction == "left":
            return self.left()
        if direction == "right":
            return self.right()

    def get_opposite(self, direction):
        if direction == "right":
            return self.left()
        if direction == "left":
            return self.right()


def parse_node(line: str):
    name, data = line.split(": ")
    if data.isnumeric():
        return node(name, int(data), None, None, None)
    left, operator, right = data.split()
    return node(name, None, left, right, operator)


def solve_equation(unknown_side, operand, operator, result):
    if operator == "+":
        return result - operand  # x + 2 = 4 => x = 4 - 2
    if operator == "-":
        if unknown_side == "left":
            return result + operand  # x - 2 = 4 => x = 4 + 2
        if unknown_side == "right":
            return operand - result  # 2 - x = 4 => x = 2 - 4
    if operator == "*":
        return result / operand  # x * 2 = 4 => x = 4 / 2
    if operator == "/":
        if unknown_side == "left":
            return result * operand  # x / 2 = 4 => x = 4 * 2
        if unknown_side == "right":
            return operand / result  # 2 / x = 4 => x = 2 / 4


def find_value():
    steps = node.all_nodes["humn"].get_steps()
    root_node = node.all_nodes["root"]
    unknown_side = steps.pop(0)
    unknown = root_node.get_child(unknown_side)
    value = root_node.get_opposite(unknown_side).get_value()

    while unknown.name != "humn":
        unknown_side = steps.pop(0)
        operand, operator = unknown.get_opposite(unknown_side).get_value(), unknown.operator
        value = solve_equation(unknown_side, operand, operator, value)
        unknown = unknown.get_child(unknown_side)
    return value


def main():
    with open("input_day_21.txt") as file:
        for line in file.read().splitlines():
            parse_node(line)
    print(node.all_nodes["root"].get_value())
    print(find_value())


main()
