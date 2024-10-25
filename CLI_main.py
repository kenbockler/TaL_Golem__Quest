# Define the crystal effects on platforms
# Each crystal affects specific platforms by changing their level by one step in the cycle (0 → 1 → 2 → 0)
# Crystal 1 affects platform 1 and 3
# Crystal 2 affects platform 2 and 3
# Crystal 3 affects platform 2 and 4
# Crystal 4 affects platform 1, 3, and 5
# Crystal 5 affects platform 4 and 5

# Maatriks A defineerib milliseid platvorme iga kristall mõjutab:
# Crystal 1 affects platforms 1 and 3
# Crystal 2 affects platforms 2 and 3
# Crystal 3 affects platforms 2 and 4
# Crystal 4 affects platforms 1, 3, and 5
# Crystal 5 affects platforms 4 and 5

A = [
    [1, 0, 0, 1, 0],  # Platform 1 affected by Crystal 1 and Crystal 4
    [0, 1, 1, 0, 0],  # Platform 2 affected by Crystal 2 and Crystal 3
    [1, 1, 0, 1, 0],  # Platform 3 affected by Crystal 1, Crystal 2, and Crystal 4
    [0, 0, 1, 0, 1],  # Platform 4 affected by Crystal 3 and Crystal 5
    [0, 0, 0, 1, 1],  # Platform 5 affected by Crystal 4 and Crystal 5
]

# Base heights of the platforms
# These heights represent the constant base height of each platform (0, 2, 1, 0, 2)
# These base heights will be added to the user-provided initial levels
base_heights = [0, 2, 1, 0, 2]

def mod_inv(a, m):
    """Compute the modular inverse of a under modulo m."""
    for x in range(m):
        if (a * x) % m == 1:
            return x
    return None  # No inverse if a and m are not coprime

def gaussian_elimination_mod3(A, b):
    """Perform Gaussian elimination modulo 3 on matrix A with vector b."""
    n = len(b)
    # Augment the matrix A with the vector b
    for i in range(n):
        A[i].append(b[i])
    # Forward elimination
    for i in range(n):
        # Find pivot for column i
        pivot = None
        for j in range(i, n):
            if A[j][i] % 3 != 0:
                pivot = j
                break
        if pivot is None:
            continue
        # Swap rows if necessary
        if pivot != i:
            A[i], A[pivot] = A[pivot], A[i]
        # Normalize pivot row
        inv = mod_inv(A[i][i] % 3, 3)
        if inv is None:
            continue
        for k in range(i, n + 1):
            A[i][k] = (A[i][k] * inv) % 3
        # Eliminate below
        for j in range(i + 1, n):
            factor = A[j][i]
            for k in range(i, n + 1):
                A[j][k] = (A[j][k] - factor * A[i][k]) % 3
    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = A[i][n]
        for j in range(i + 1, n):
            x[i] = (x[i] - A[i][j] * x[j]) % 3
    return x

def main():
    print("\nNote: Platform numbering is from left to right, as well as crystal numbering.")

    # Request initial levels for each platform
    # Levels: 0 - Golem crouching fully, 1 - Golem half-crouch, 2 - Golem standing fully
    initial_levels = []
    for i in range(5):
        while True:
            try:
                # Ask for user input and explain the meanings of each level
                level = int(input(f"Enter initial level for platform {i+1} (0 for crouch, 1 for half-crouch, 2 for stand): "))
                if level in [0, 1, 2]:  # Only allow valid inputs
                    initial_levels.append(level)
                    break
                else:
                    print("Please enter a valid level (0 for crouch, 1 for half-crouch, 2 for stand).")
            except ValueError:
                print("Invalid input. Please enter an integer.")

    # Try each possible target height H to equalize all platform heights
    found_solution = False
    for H in range(5):  # Try H values from 0 to 4
        # Calculate constants needed for each platform
        # Constant 'c_i' is the required height mod 3, minus the base height and initial level
        c = [(H - base_heights[i]) % 3 for i in range(5)]
        rhs = [(c[i] - initial_levels[i]) % 3 for i in range(5)]

        # Copy matrix A for manipulation during elimination
        A_copy = [row[:] for row in A]
        augmented_matrix = [A_copy[i] + [rhs[i]] for i in range(5)]

        # Solve using Gaussian elimination modulo 3
        try:
            # Attempt to solve the system for a consistent solution
            x = gaussian_elimination_mod3([row[:] for row in A_copy], rhs[:])
            # Check if solution x is valid (all values are within 0, 1, or 2)
            if all(0 <= xi <= 2 for xi in x):
                # Verify that all platform heights reach the target height H
                total_heights = []
                for i in range(5):
                    lever_sum = sum(A[i][j] * x[j] for j in range(5)) % 3
                    s_i = (initial_levels[i] + lever_sum) % 3
                    total_height = base_heights[i] + s_i
                    total_heights.append(total_height)
                if all(th == H for th in total_heights):
                    print("\nSolution found:")
                    for j in range(5):
                        print(f"Press crystal {j+1}: {x[j]} times")
                    found_solution = True
                    break
        except:
            continue
    # If no solution found, notify the user
    if not found_solution:
        print("No solution found to equalize all platform heights.")

if __name__ == "__main__":
    main()
