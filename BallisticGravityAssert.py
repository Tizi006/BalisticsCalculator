from scipy.optimize import minimize
import numpy as np
from BalisticsCalculation import solve_ballistic_arc


def find_gravity(shooter, target, power, angle):
    def objective(gravity):
        gravity_unpacked = float(gravity[0])
        angle1, angle2 = solve_ballistic_arc(shooter, target, power, gravity_unpacked)
        if angle1 is None or angle2 is None:
            return 1e6  # A large penalty
        return min(abs(angle1 - angle), abs(angle2 - angle))  # Minimize the difference

    arr = np.ndarray(1)
    arr[0] = 8
    # Use an optimization algorithm to find the gravity that minimizes the error
    result = minimize(objective, x0=0.1, bounds=[(0.1, 10)])
    return result.x[0]  # Optimized gravity


# Function to assert test values to inputs
def run_test():
    # Example test sets
    test_sets = [
        # really short
        {'shooter': (429, 1071), 'target': (626, 1080), 'power': 25, 'target_angle': 25},
        # mid
        {'shooter': (620, 1072), 'target': (1493, 1081), 'power': 50, 'target_angle': 45},
        # long
        {'shooter': (620, 1072), 'target': (2292, 1053), 'power': 100, 'target_angle': 75},
        # special angles
        {'shooter': (429, 1072), 'target': (2490, 265), 'power': 100, 'target_angle': 45},
        {'shooter': (429, 1072), 'target': (2421, 650), 'power': 100, 'target_angle': 70},
    ]

    # Calculate gravity for each test set
    for item in test_sets:
        result = find_gravity(item['shooter'], item['target'], item['power'], item['target_angle'])
        print(result)


run_test()
