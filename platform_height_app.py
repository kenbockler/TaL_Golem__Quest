import streamlit as st

# Define platform base heights and crystal effects
base_heights = [0, 2, 1, 0, 2]
A = [
    [1, 0, 0, 1, 0],  # Platform 1 affected by Crystal 1 and Crystal 4
    [0, 1, 1, 0, 0],  # Platform 2 affected by Crystal 2 and Crystal 3
    [1, 1, 0, 1, 0],  # Platform 3 affected by Crystal 1, Crystal 2, and Crystal 4
    [0, 0, 1, 0, 1],  # Platform 4 affected by Crystal 3 and Crystal 5
    [0, 0, 0, 1, 1],  # Platform 5 affected by Crystal 4 and Crystal 5
]

# Utility functions for modular inverse and Gaussian elimination
def mod_inv(a, m):
    for x in range(m):
        if (a * x) % m == 1:
            return x
    return None

def gaussian_elimination_mod3(A, b):
    n = len(b)
    for i in range(n):
        A[i].append(b[i])
    for i in range(n):
        pivot = None
        for j in range(i, n):
            if A[j][i] % 3 != 0:
                pivot = j
                break
        if pivot is None:
            continue
        if pivot != i:
            A[i], A[pivot] = A[pivot], A[i]
        inv = mod_inv(A[i][i] % 3, 3)
        if inv is None:
            continue
        for k in range(i, n + 1):
            A[i][k] = (A[i][k] * inv) % 3
        for j in range(i + 1, n):
            factor = A[j][i]
            for k in range(i, n + 1):
                A[j][k] = (A[j][k] - factor * A[i][k]) % 3
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = A[i][n]
        for j in range(i + 1, n):
            x[i] = (x[i] - A[i][j] * x[j]) % 3
    return x

# Streamlit UI
st.title("Platform Height Equalizer with Crystals")
st.markdown("### Instructions")
st.markdown("Platform and crystal numbering starts from the left and goes to the right. Set the initial levels for each platform below:")

# Input fields for initial platform levels
initial_levels = []
for i in range(5):
    level = st.selectbox(
        f"Initial level for Platform {i+1}:",
        options=[0, 1, 2],
        format_func=lambda x: ["Crouch (0)", "Half-crouch (1)", "Stand (2)"][x],
        key=f"platform_{i}"
    )
    initial_levels.append(level)

# Processing and output
if st.button("Calculate"):
    found_solution = False
    for H in range(5):
        c = [(H - base_heights[i]) % 3 for i in range(5)]
        rhs = [(c[i] - initial_levels[i]) % 3 for i in range(5)]
        A_copy = [row[:] for row in A]
        try:
            x = gaussian_elimination_mod3([row[:] for row in A_copy], rhs[:])
            if all(0 <= xi <= 2 for xi in x):
                total_heights = []
                for i in range(5):
                    lever_sum = sum(A[i][j] * x[j] for j in range(5)) % 3
                    s_i = (initial_levels[i] + lever_sum) % 3
                    total_height = base_heights[i] + s_i
                    total_heights.append(total_height)
                if all(th == H for th in total_heights):
                    st.success("Solution found! Press each crystal as follows:")
                    # Display result from left to right
                    result_text = " | ".join([f"Crystal {j+1}: {x[j]} presses" for j in range(5)])
                    st.markdown(f"**{result_text}**")
                    found_solution = True
                    break
        except:
            continue
    if not found_solution:
        st.error("No solution found to equalize all platform heights.")
