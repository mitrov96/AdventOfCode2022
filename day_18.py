with open('input_day_18.txt') as f:
    coords = set()
    for line in f.readlines():
        line = line.strip()
        x, y, z = line.split(",")
        coords.add((int(x), int(y), int(z)))

    adjacent_coords = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
    surface_area = 0
    for coord in coords:
        area = 6
        x, y, z = coord
        for dv in adjacent_coords:
            dx, dy, dz = dv
            if (x + dx, y + dy, z + dz) in coords:
                area -= 1
        surface_area += area

    print(f"Part 1: surface area is {surface_area}")

    external_points = set()
    external_area = 0
    for coord in coords:
        area = 6
        x, y, z = coord
        for dv in adjacent_coords:
            dx, dy, dz = dv
            if (x + dx, y + dy, z + dz) in coords:
                area -= 1
            else:
                external_points.add((x + dx, y + dy, z + dz))

    cavity_points = set()
    for p in external_points:
        # outer boundary points have at least one direction where no point in the volume has a greater value in
        # that direction
        x, y, z = p
        x1, x2, y1, y2, z1, z2 = False, False, False, False, False, False
        for interal in coords:
            # cavity points: there will exist x1,x2,y1,y2,z1,z2 s.t. x1 < x < x2, y1 < y < y2, z1 < z < z2
            xi, yi, zi = interal
            if xi < x and yi == y and zi == z:
                x1 = True
            elif xi > x and yi == y and zi == z:
                x2 = True
            if yi < y and xi == x and zi == z:
                y1 = True
            elif yi > y and xi == x and zi == z:
                y2 = True
            if zi < z and xi == x and yi == y:
                z1 = True
            elif zi > z and xi == x and yi == y:
                z2 = True
        if x1 and x2 and y1 and y2 and z1 and z2:
            cavity_points.add(p)

    print(len(external_points))
    surface_area = 0
    for coord in coords:
        area = 6
        x, y, z = coord
        for dv in adjacent_coords:
            dx, dy, dz = dv
            adj_p = (x + dx, y + dy, z + dz)
            if adj_p in coords | cavity_points:
                area -= 1
        surface_area += area
    print(surface_area)
