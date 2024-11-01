import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

# Assumptions:
# - distances between pairs of beacons are unique
#
# Use distances between beacons to match beacons
# across scanner borders.
#
# Since distances are unique -> the squares of distances are too.
# Use squared distances to prevent unneeded sqrt calls
#
# Distances are independent from coordinate system.
# Eq. does not matter which position and orientation the scanner has.


# Only when two scanners have enough matching pairs, their relative poses are defined
# n beacons have 1+2+...+(n-1) pairs -> use gauss formal
MIN_BEACON_MATCHES = 12
MIN_PAIR_MATCHES = MIN_BEACON_MATCHES * (MIN_BEACON_MATCHES - 1) // 2

# Define all 24 possible orientation matrices
IDENTITY = np.eye(3, dtype=np.int32)
ORIENTATIONS = []
for x in range(3):
    for y in filter(lambda i: i != x, range(3)):
        for x_sign in (-1, 1):
            for y_sign in (-1, 1):
                A = np.zeros(shape=(3, 3), dtype=np.int32)
                # Pick unit vector along the x, y-th dimension
                # cross product produces right-hand system as needed
                A[:, 0] = x_sign * IDENTITY[:, x]
                A[:, 1] = y_sign * IDENTITY[:, y]
                A[:, 2] = np.cross(A[:, 0], A[:, 1])
                ORIENTATIONS.append(A)


@dataclass
class Scanner:
    beacons: List[np.ndarray]
    distance_map: Dict[int, Tuple[np.ndarray, np.ndarray]]
    position: np.ndarray | None
    orientation: np.ndarray | None


def parse_scanner(text: str):
    beacons = []
    for line in text.splitlines()[1:]:
        position = list(map(int, line.split(",")))
        beacons.append(np.array(position, dtype=np.int32))

    distance_map = {}
    for i_src, src in enumerate(beacons):
        for dest in beacons[i_src+1:]:
            rel = dest - src
            dist = int(np.dot(rel, rel))
            assert dist not in distance_map
            distance_map[dist] = (src, dest)

    return Scanner(beacons, distance_map, None, None)


def overlapping_scanners(scanners: List[Scanner]):
    result: Dict[Tuple[int, int], Set[int]] = {}
    for i_src, src in enumerate(scanners):
        src_distances = set(src.distance_map.keys())

        for i_dest, dest in enumerate(scanners):
            # Only check every pair of scanner once
            if i_src >= i_dest:
                continue

            dest_distances = set(dest.distance_map.keys())
            common = src_distances.intersection(dest_distances)

            if len(common) >= MIN_PAIR_MATCHES:
                result[(i_src, i_dest)] = common
    return result


def locate_scanners(scanners: List[Scanner]):
    # Scanner poses are relative, use the first scanner's pose as origin
    scanners[0].position = np.zeros(shape=(3,), dtype=np.int32)
    scanners[0].orientation = IDENTITY
    scanners_located = 1

    # Find overlapping pairs, for every pair the relative pose can be computed
    overlaps = overlapping_scanners(scanners)

    # A pair is solvable if one scanners is already located
    def can_solve(indices):
        src, dest = indices
        return (scanners[src].position is None) != (scanners[dest].position is None)

    # Check, if both positions yield the same relative scanner position
    def try_relative_scanner_position(solved1, solved2, unsolved1, unsolved2):
        for u1, u2 in [(unsolved1, unsolved2), (unsolved2, unsolved1)]:
            rel1 = solved1 - u1
            rel2 = solved2 - u2
            error = rel1 - rel2
            if not np.dot(error, error):
                return rel1

    # Locate one scanner at a time until all are located
    while scanners_located < len(scanners):
        pair = next(filter(can_solve, overlaps.keys()))

        # Determine which scanner in the pair is solved and which needs to be located
        solved_idx = 1 if scanners[pair[0]].position is None else 0
        solved_scanner = scanners[pair[solved_idx]]
        unsolved_scanner = scanners[pair[1 - solved_idx]]

        # Brute force all 24 orientations untill the correct one of the unsolved scanner is found
        # The position of the unsolved scanner is computed along the way
        for A in ORIENTATIONS:

            # Every matching relative pair must be equal by applying the correct orientation
            found = True
            for dist in overlaps[pair]:
                solved1, solved2 = solved_scanner.distance_map[dist]
                unsolved1, unsolved2 = unsolved_scanner.distance_map[dist]

                relative = try_relative_scanner_position(
                    solved_scanner.orientation @ solved1, solved_scanner.orientation @ solved2, A @ unsolved1, A @ unsolved2)

                # Abort if the orientation violates one pair
                if relative is None:
                    found = False
                    break

                # If the orientation solves this pair keep track of the corresponding position
                # On the correct orientation the position will be the same for all pairs
                else:
                    unsolved_scanner.position = solved_scanner.position + relative

            # When the current orientation solves the location the scanner is fully located
            if found:
                unsolved_scanner.orientation = A
                break

        scanners_located += 1


def merge_beacons(scanners: List[Scanner]):
    # Produce a unique set of absolute beacon positions
    beacons = set()
    for scanner in scanners:
        for beacon in scanner.beacons:
            beacons.add(tuple(scanner.position + scanner.orientation @ beacon))
    return beacons


scanners = [parse_scanner(t) for t in open(0).read().split("\n\n")]
locate_scanners(scanners)
beacons = merge_beacons(scanners)
print("part1:", len(beacons))

part2 = 0
for i, s1 in enumerate(scanners):
    for s2 in scanners[i+1:]:
        rel = s1.position - s2.position
        part2 = max(part2, np.sum(np.abs(rel)))
print("part2:", part2)
