import math


def solve_ballistic_arc(shooter, target, power, gravity):
    # Shooter and Target coordinates
    x1, y1 = shooter
    x2, y2 = target
    # Calculate the horizontal and vertical distances
    dx = math.fabs(x2 - x1)
    dy = y1 - y2
    # Distance of vector between shooter and target using Pythagorean theorem
    # (currently not used, got better results with dx)
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # variables for calculation
    speed2 = power ** 2
    speed4 = power ** 4

    root = speed4 - gravity * (gravity * dx * dx + 2 * dy * speed2)

    # No Solution
    if root < 0:
        return None, None

    rooted_root = math.sqrt(root)

    low_angle_rad = math.atan2(speed2 - rooted_root, gravity * dx)
    high_angle_rad = math.atan2(speed2 + rooted_root, gravity * dx)

    # Convert to degrees
    low_angle_deg = math.degrees(low_angle_rad)
    high_angle_deg = math.degrees(high_angle_rad)

    return low_angle_deg, high_angle_deg
