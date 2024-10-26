from math import sqrt


def parse(line):
    coords = line.split(": ")[1]
    x, y = coords.split(", ")

    def get_range(text):
        text = text.split("=")[1]
        values = text.split("..")
        return int(values[0]), int(values[1])

    return get_range(x), get_range(y)


target_def = next(open(0))
area = parse(target_def)


def find_max_init_vel_y(area):
    _, (area_y_min, _) = area
    return -area_y_min - 1


def get_apex_y(init_vel_y):
    return init_vel_y * (init_vel_y + 1) // 2


max_init_vel_y = find_max_init_vel_y(area)
print("part1:", get_apex_y(max_init_vel_y))


def hits_area(area, init_vel):
    pos_x, pos_y = 0, 0
    (area_x_min, area_x_max), (area_y_min, area_y_max) = area
    vel_x, vel_y = init_vel

    while pos_x <= area_x_max and pos_y >= area_y_min:
        if pos_x >= area_x_min and pos_y <= area_y_max:
            return True     # in area

        pos_x += vel_x
        pos_y += vel_y
        vel_x = 0 if vel_x == 0 else vel_x - 1
        vel_y -= 1  # gravity

    return False


(area_min_x, max_init_vel_x), (min_init_vel_y, _) = area
min_init_vel_x = int((sqrt(1 + 8*area_min_x) - 1) // 2)

possibilities = 0
for init_vel_x in range(min_init_vel_x, max_init_vel_x + 1):
    for init_vel_y in range(min_init_vel_y, max_init_vel_y + 1):
        if hits_area(area, (init_vel_x, init_vel_y)):
            possibilities += 1
print("part2:", possibilities)
