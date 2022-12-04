def main():
    in_file = open('input_day_4.txt', 'r')
    overlap = 0

    for line in in_file:
        entry1 = line.strip().split(',')[0]
        start1 = entry1.split('-')[0]
        end1 = entry1.split('-')[1]

        entry2 = line.strip().split(',')[1]
        start2 = entry2.split('-')[0]
        end2 = entry2.split('-')[1]

        range1 = list()

        for idx in range(int(start1), int(end1) + 1):
            range1.append(idx)

        range2 = list()

        for jdx in range(int(start2), int(end2) + 1):
            range2.append(jdx)

        intersect = set(range1).intersection(set(range2))

        if len(intersect) != 0:
            overlap = overlap + 1

    print(overlap)


main()
