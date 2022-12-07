file = "input_day_7.txt"


class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = {}

    def __str__(self) -> str:
        return f"{self.name}: {self.totalSize()}"

    def __repr__(self) -> str:
        return str(self)

    def totalSize(self):
        size = 0
        for c in self.children.values():
            if isinstance(c, Dir):
                size += c.totalSize()
            elif isinstance(c, File):
                size += c.size

        return size

    def count(self):
        total = 0
        if self.totalSize() <= 10000:
            total = 1

        for d in (d for d in self.children.values() if isinstance(d, Dir)):
            total += d.count()

        return total

    def findSmallDirs(self):
        ret = []
        if self.totalSize() <= 100000:
            ret.append(self)

        for d in (d for d in self.children.values() if isinstance(d, Dir)):
            ret += d.findSmallDirs()

        return ret


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


root = Dir("", None)

curDir = root

allDirs = [root]

with open(file, mode="rt", encoding="utf-8") as file:
    for line in (line.strip() for line in file):
        if len(line) == 0:
            continue

        args = line.split(" ")
        if args[0] == "$":
            if args[1] == "cd":
                if args[2] == "/":
                    curDir = root
                elif args[2] == "..":
                    curDir = curDir.parent
                else:
                    curDir = curDir.children[args[2]]
            elif args[1] == "ls":
                # Nothing
                pass

        elif args[0] == "dir":
            curDir.children[args[1]] = Dir(args[1], curDir)
            allDirs.append(curDir.children[args[1]])

        else:
            curDir.children[args[1]] = File(args[1], int(args[0]))

totalSpace = 70000000
freeSpace = totalSpace - root.totalSize()
reqSpace = 30000000 - freeSpace

allDirs.sort(key=lambda d: d.totalSize())
allDirs = [d for d in allDirs if d.totalSize() >= reqSpace]
print(allDirs[0].totalSize())
