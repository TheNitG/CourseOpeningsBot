import sys
from collections import deque

sys.setrecursionlimit(50000)
length = int()
N = int()
subblock_height = int()
subblock_width = int()
symbol_set = set()
constraints = dict()
propagation = dict()
calls = 0
rows = dict()
cols = dict()
boxes = dict()


async def sudoku_solve(message, puzzle):
    global length, N, subblock_height, subblock_width, symbol_set, constraints, calls, propagation, rows, cols
    available_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    puzzle = puzzle.rstrip()
    length = len(puzzle)
    N = int(length ** (1 / 2))
    for x in range(int(N ** (1 / 2)), N + 1):
        if N % x == 0:
            subblock_height = x
            break
    subblock_width = N // subblock_height
    symbol_set = set(available_chars[:N])
    constraints = make_constraint_dict()
    calls = 0
    puzzle = constraint_propagation(puzzle)
    puzzle = optimized_handler(puzzle)
    solution = csp_propagation_optimization_b(puzzle)
    output = print_board(solution)
    await message.channel.send('```' + output + '```')


def constraint_propagation(state):
    global constraints, symbol_set, propagation
    solved = deque()
    visited = set()
    for index in constraints:
        if state[index] != ".":
            propagation[index] = set(state[index])
            solved.append(index)
            visited.add(index)
            continue
        propagation[index] = symbol_set.copy()
    while solved:
        solved_index = solved.popleft()
        for constraint in constraints[solved_index]:
            propagate = propagation[constraint]
            to_remove = state[solved_index]
            if to_remove in propagate:
                propagate.remove(to_remove)
                propagation[constraint] = propagate
                if len(propagate) == 1:
                    state = state[:constraint] + "".join(propagate) + state[constraint + 1:]
                    solved.append(constraint)
                    visited.add(constraint)
    return logic_piece_2(state)


def logic_piece_1(state):
    global constraints, symbol_set, propagation
    solved = deque()
    for index in constraints:
        if len(propagation[index]) == 1:
            solved.append(index)
    while solved:
        solved_index = solved.popleft()
        for constraint in constraints[solved_index]:
            propagate = propagation[constraint]
            to_remove = state[solved_index]
            if to_remove in propagate:
                propagate.remove(to_remove)
                propagation[constraint] = propagate
                if len(propagate) == 0:
                    return None
                if len(propagate) == 1:
                    state = state[:constraint] + "".join(propagate) + state[constraint + 1:]
                    solved.append(constraint)
    return state


def logic_piece_2(state):
    global propagation, constraints, symbol_set, rows, cols, boxes
    for row in rows:
        for char in symbol_set:
            appears = 0
            possible = -1
            for index in rows[row]:
                if char in propagation[index]:
                    if appears == 1:
                        appears = 0
                        break
                    appears = 1
                    possible = index
            if appears == 1:
                propagation[possible] = set(char)
                state = state[:possible] + char + state[possible + 1:]
    for col in cols:
        for char in symbol_set:
            appears = 0
            possible = -1
            for index in cols[col]:
                if char in propagation[index]:
                    if appears == 1:
                        appears = 0
                        break
                    appears = 1
                    possible = index
            if appears == 1:
                propagation[possible] = set(char)
                state = state[:possible] + char + state[possible + 1:]
    for box in boxes:
        for char in symbol_set:
            appears = 0
            possible = -1
            for index in boxes[box]:
                if char in propagation[index]:
                    if appears == 1:
                        appears = 0
                        break
                    appears = 1
                    possible = index
            if appears == 1:
                propagation[possible] = set(char)
                state = state[:possible] + char + state[possible + 1:]
    return logic_piece_1(state)


def logic_piece_1_optimized(state):
    changed = False
    global constraints, symbol_set, propagation
    solved = deque()
    for index in constraints:
        if len(propagation[index]) == 1:
            solved.append(index)
    while solved:
        solved_index = solved.popleft()
        for constraint in constraints[solved_index]:
            propagate = propagation[constraint]
            to_remove = state[solved_index]
            if to_remove in propagate:
                changed = True
                propagate.remove(to_remove)
                propagation[constraint] = propagate
                if len(propagate) == 0:
                    return None, None
                if len(propagate) == 1:
                    state = state[:constraint] + "".join(propagate) + state[constraint + 1:]
                    solved.append(constraint)
    return state, changed


def logic_piece_2_optimized(state):
    global propagation, constraints, symbol_set, rows, cols, boxes
    for row in rows:
        for char in symbol_set:
            appears = 0
            possible = -1
            for index in rows[row]:
                if char in propagation[index]:
                    if appears == 1:
                        appears = 0
                        break
                    appears = 1
                    possible = index
            if appears == 1:
                propagation[possible] = set(char)
                state = state[:possible] + char + state[possible + 1:]
    for col in cols:
        for char in symbol_set:
            appears = 0
            possible = -1
            for index in cols[col]:
                if char in propagation[index]:
                    if appears == 1:
                        appears = 0
                        break
                    appears = 1
                    possible = index
            if appears == 1:
                propagation[possible] = set(char)
                state = state[:possible] + char + state[possible + 1:]
    for box in boxes:
        for char in symbol_set:
            appears = 0
            possible = -1
            for index in boxes[box]:
                if char in propagation[index]:
                    if appears == 1:
                        appears = 0
                        break
                    appears = 1
                    possible = index
            if appears == 1:
                propagation[possible] = set(char)
                state = state[:possible] + char + state[possible + 1:]
    return state


def optimized_handler(state):
    state, changed = logic_piece_1_optimized(state)
    if state is None:
        return None
    while changed:
        state = logic_piece_2_optimized(state)
        if state is None:
            return None
        state, changed = logic_piece_1_optimized(state)
        if state is None:
            return None
    return state


def make_constraint_dict():
    boxes = dict()
    constraints = dict()
    propagation = dict()
    for x in range(length):
        row = x // N
        col = x % N
        if row in rows:
            rows[row].add(x)
        else:
            rows[row] = {x}
        if col in cols:
            cols[col].add(x)
        else:
            cols[col] = {x}
    offset = 0
    remaining = [x for x in range(length)]
    for times in range(subblock_width):
        for height in range(subblock_height):
            for box in range(subblock_height):
                box += offset
                if box in boxes:
                    boxes[box] += remaining[:subblock_width]
                else:
                    boxes[box] = remaining[:subblock_width]
                remaining = remaining[subblock_width:]
        offset += subblock_height
    for box in boxes:
        box_constraints = set(boxes[box])
        for index in box_constraints:
            constraints[index] = box_constraints.copy()
            constraints[index].remove(index)
    for x in range(length):
        row = x // N
        col = x % N
        current_constraints = set()
        for y in range(N):
            current_constraints.add(row * N + y)  # For all in same row
            current_constraints.add(N * y + col)  # For all in same column
        current = constraints[x].union(set(current_constraints))
        current.remove(x)
        constraints[x] = current
    return constraints


def print_board(state):
    output = ''
    for x in range(N):
        for y in range(N):
            output += state[x * N + y] + ' '
        output += '\n'
    return output


def get_next_unassigned_var(state):
    if "." in state:
        return state.index(".")
    else:
        return -1


"""
Method that finds the first empty row going down
"""


def get_most_constrained_var():
    global propagation
    min_var = -1
    min_size = float("Inf")
    for propagate in propagation:
        size = len(propagation[propagate])
        if size == 1:
            continue
        if size == 2:
            return propagate
        if size < min_size:
            min_var = propagate
            min_size = size
    return min_var


def get_sorted_values(state, var):
    available = symbol_set.copy()
    for constraining in constraints[var]:
        if state[constraining] in available:
            available.remove(state[constraining])
    return available


"""
Method that finds all safe columns for a queen on row var
"""


def goal_test(state):
    return "." not in state


"""
Checks if the Sudoku puzzle has been solved
"""


def result_test(state):
    if "." in state:
        return False
    for index in constraints:
        for constraint in constraints[index]:
            if state[index] == state[constraint]:
                return False
    return True


"""
Checks if the Sudoku puzzle has been solved
"""


def csp(state):
    global calls
    calls += 1
    if goal_test(state):
        return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        result = csp(state[:var] + val + state[var + 1:])
        if result is not None:
            return result
    return None


"""
Method that recursively uses a depth-first-search to find the possible Sudoku solution
"""


def csp_propagation(state):
    global calls, propagation
    calls += 1
    if goal_test(state):
        return state
    var = get_most_constrained_var()
    for val in propagation[var].copy():
        temp_propagation = dict()
        for propagate in propagation:
            temp_propagation[propagate] = propagation[propagate].copy()
        new_state = state[:var] + val + state[var + 1:]
        propagation[var] = set(val)
        new_state = logic_piece_1(new_state)
        if new_state is None:
            propagation = temp_propagation
            continue
        if goal_test(new_state):
            return new_state
        result = csp_propagation(new_state)
        if result is not None:
            return result
        propagation = temp_propagation
    return None


"""
Method that recursively uses a depth-first-search to find the possible Sudoku solution
"""


def csp_propagation_part_2(state):
    global calls, propagation
    calls += 1
    if goal_test(state):
        return state
    var = get_most_constrained_var()
    for val in propagation[var].copy():
        temp_propagation = dict()
        for propagate in propagation:
            temp_propagation[propagate] = propagation[propagate].copy()
        new_state = state[:var] + val + state[var + 1:]
        propagation[var] = set(val)
        new_state = logic_piece_1(new_state)
        if new_state is None:
            propagation = temp_propagation
            continue
        new_state = logic_piece_2(new_state)
        if new_state is None:
            propagation = temp_propagation
            continue
        if goal_test(new_state):
            return new_state
        result = csp_propagation_part_2(new_state)
        if result is not None:
            return result
        propagation = temp_propagation
    return None


"""
Method that recursively uses a depth-first-search to find the possible Sudoku solution
"""


def csp_propagation_optimization_b(state):
    global calls, propagation
    calls += 1
    if goal_test(state):
        return state
    var = get_most_constrained_var()
    for val in propagation[var].copy():
        temp_propagation = dict()
        for propagate in propagation:
            temp_propagation[propagate] = propagation[propagate].copy()
        new_state = state[:var] + val + state[var + 1:]
        propagation[var] = set(val)
        new_state = optimized_handler(new_state)
        if new_state is None:
            propagation = temp_propagation
            continue
        if goal_test(new_state):
            return new_state
        result = csp_propagation_optimization_b(new_state)
        if result is not None:
            return result
        propagation = temp_propagation
    return None


"""
Method that recursively uses a depth-first-search to find the possible Sudoku solution
"""
