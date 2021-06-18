'''
Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state). You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.
Write a function answer(m) that takes an array of array of non-negative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. For example, consider the matrix m:

[
    [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
    [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
    [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
    [0,0,0,0,0,0],  # s3 is terminal
    [0,0,0,0,0,0],  # s4 is terminal
    [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of [s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is [0, 3, 2, 9, 14].
'''

import numpy as np
from fractions import Fraction

def solution(m):
    # To find limiting matrices for absorbing Markov Chains, we want to break our
    # transition matrix (m) into a standard form by calculating each submatrix, shown below:
    """
     Standard Form        Limiting Matrix
       | I | 0 |            |  I |  0 |
       |---|---|   ------>  |----|----|
       | R | Q |            | FR |  0 |

    """
    if len(m) <= 1 or sum(m[0]) == 0: return [1, 1]
    r_submatrix, q_submatrix = split_matrix(m)
    f_submatrix = find_f_submatrix(q_submatrix)
    fr_submatrix = np.dot(f_submatrix, r_submatrix)
    return probabilities(fr_submatrix[0])

def split_matrix(m):
    # Keep track of which states are absorbing (sets allow quick access when checking).
    absorbing_states = set()
    # Finding R and Q will help us find the limiting matrix.
    r_submatrix, q_submatrix = [], []
    # Number of rows and columns are the same since each row/column represents a state.
    num_of_rows, num_of_columns = len(m),len(m)
    # Find all absorbing states.
    for row in range(num_of_rows):
        # This state is a absorbing state if it can't go to any other states.
        if sum(m[row]) == 0:
            absorbing_states.add(row)
    # Split the matrix into R and Q
    for row in range(num_of_rows):
        # All absorbing states would be in the identity matrix in a standard form, so only check for non-absorbing states.
        if row not in absorbing_states:
            # Used to get the decimal number and eventually gets us our denominator.
            total_transitions = float(sum(m[row]))
            temp_r, temp_q = [], []
            # Goes through the probabilities of the current state going to all other states.
            for col in range(num_of_columns):
                # R submatrix will be used to keep track of the chances of current state going into a absorbing state.
                if col in absorbing_states:
                    temp_r.append(m[row][col] / total_transitions)
                else:
                    temp_q.append(m[row][col] / total_transitions)
            r_submatrix.append(temp_r)
            q_submatrix.append(temp_q)
    return r_submatrix, q_submatrix

def find_f_submatrix(q_submatrix):
    # The equation to find the F submatrix is: F = (I - Q) ^ -1, so the steps are as follows:
    # 1. Find the identity matrix
    # 2. Subtract Q submatrix from the identity matrix.
    # 3. Find the inverse of the difference.
    size_of_q = len(q_submatrix)
    identity_matrix = np.identity(size_of_q)
    difference_between_identity_and_q = np.subtract(identity_matrix, q_submatrix)
    return np.linalg.inv(difference_between_identity_and_q)

def probabilities(row):
    # First row of FR we have the probabilities of reaching terminal states, which we now have to convert to fractions.
    probabilities_for_each_state, denominators = [], []
    for num in row:
        fraction = Fraction(num).limit_denominator()
        probabilities_for_each_state.append(fraction.numerator)
        denominators.append(fraction.denominator)
    # Find the next smallest integer that's divisible by both current lcd and the denominator.
    lcd = 1
    for denom in denominators:
        temp_lcd = lcd
        temp_denom = denom
        while temp_denom:
            temp_lcd, temp_denom = temp_denom, temp_lcd % temp_denom
        lcd = lcd // temp_lcd * denom
    # Multiply the previous numerators we found by the lcd so they are simplified correctly.
    for num in range(len(probabilities_for_each_state)):
        probabilities_for_each_state[num] *= int(lcd / denominators[num])
    # Adds the least common denominator to the end.
    probabilities_for_each_state.append(lcd)
    return probabilities_for_each_state


t1 = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]
t1_check = solution(t1) == [7, 6, 8, 21]

t2 = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
t2_check = solution(t2) == [0, 3, 2, 9, 14]


# Great explaination and test cases here:
# - https://github.com/ivanseed/google-foobar-help/blob/master/challenges/doomsday_fuel/doomsday_fuel.md
# - https://pages.cs.wisc.edu/~shrey/2020/08/10/google-foobar.html
# - https://sskaje.me/2017/05/googles-foo-bar-doomsday-fuel/
