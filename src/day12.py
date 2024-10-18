def add_link(map, src, dest):
    targets = map.get(src, [])
    targets.append(dest)
    map[src] = targets


map = {}
for line in open(0):
    src, dest = line.rstrip().split("-")
    add_link(map, src, dest)
    add_link(map, dest, src)


def solve_dfs(node, visited, revisted_node):
    if node == "end":
        return 1

    track_node = node.islower()
    if track_node and node in visited:
        if revisted_node is None and node != "start":
            revisted_node = node
        else:
            return 0

    if track_node:
        visited.add(node)

    path_count = 0
    for target in map[node]:
        path_count += solve_dfs(target, visited, revisted_node)

    if track_node and revisted_node != node:
        visited.remove(node)

    return path_count


print("part1:", solve_dfs("start", set(), ""))
print("part2:", solve_dfs("start", set(), None))
