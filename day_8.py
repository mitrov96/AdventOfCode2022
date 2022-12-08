trees = []
visibility = []


def parse_line(line):
    global trees
    these = []
    for c in line:
        these.append(int(c))
    trees.append(these)


def init_visibility():
    global visibility
    num_x = len(trees)
    num_y = len(trees[0])
    for y in range(num_x):
        visibility.append([0] * num_y)


def trees_visible_in_line(sx, sy, dx, dy, num):
    height = -1
    total = 0
    x = sx
    y = sy
    for i in range(num):
        ici = trees[y][x]
        if ici > height:
            visibility[y][x] = 1
        height = max(height, ici)
        x += dx
        y += dy


def mark_all_trees():
    num_x = len(trees)
    num_y = len(trees[0])
    for y in range(num_y):
        trees_visible_in_line(0, y, 1, 0, num_x)  # to the right
        trees_visible_in_line(num_x - 1, y, -1, 0, num_x)  # to the left
    for x in range(num_x):
        trees_visible_in_line(x, 0, 0, 1, num_y)  # to the bottom
        trees_visible_in_line(x, num_y - 1, 0, -1, num_y)  # to the top


def count_trees():
    return sum([sum(row) for row in visibility])


# num can be zero
def look_along(sx, sy, dx, dy, num):
    x = sx
    y = sy
    height = trees[sy][sx]
    dist = 0
    for i in range(num):
        x += dx
        y += dy
        ici = trees[y][x]
        dist += 1
        if ici >= height:
            return dist
    return dist


def scenic_score_tree(x, y):
    num_y = len(trees[0])
    num_x = len(trees)
    up = look_along(x, y, 0, -1, y)
    down = look_along(x, y, 0, 1, num_y - y - 1)
    left = look_along(x, y, -1, 0, x)
    right = look_along(x, y, 1, 0, num_x - x - 1)
    return up * down * left * right


def all_trees_scenic():
    num_y = len(trees[0])
    num_x = len(trees)
    score = 0
    for x in range(num_x):
        for y in range(num_y):
            score = max(score, scenic_score_tree(x, y))
    return score


def read_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))


def main():
    read_file('input_day_8.txt')
    init_visibility()
    mark_all_trees()
    print(count_trees())
    print(all_trees_scenic())


if __name__ == '__main__':
    main()
