import asyncio
import sys
from collections import deque
from time import perf_counter

sys.setrecursionlimit(50000)


def goal_test(board):
    if board[0:3] == "XXX" or board[3:6] == "XXX" or board[6:9] == "XXX" or board[::3] == "XXX" or board[1::3] == "XXX"\
            or board[2::3] == "XXX" or board[0] == "X" and board[4] == "X" and board[8] == "X" or board[2] == "X"\
            and board[4] == "X" and board[6] == "X":
        return "X wins"
    if board[0:3] == "OOO" or board[3:6] == "OOO" or board[6:9] == "OOO" or board[::3] == "OOO" or board[1::3] == "OOO"\
            or board[2::3] == "OOO" or board[0] == "O" and board[4] == "O" and board[8] == "O" or board[2] == "O"\
            and board[4] == "O" and board[6] == "O":
        return "O wins"
    if "." in board:
        return "Not finished"
    return "Tie"


"""
Determines whether player X wins, player O wins, the game is not completed yet, or the game has ended in a tie
"""


def possible_moves(board, turn):
    moves = set()
    for index, char in enumerate(board):
        if char == ".":
            moves.add(board[:index] + turn + board[index + 1:])
    return moves


"""
Finds all possible boards when player turn plays
"""


def distinct_games():
    queue = deque([(".........", "X")])
    count = 0
    while queue:
        current_board, current_turn = queue.popleft()
        for child_node in possible_moves(current_board, current_turn):
            if not goal_test(child_node) == "Not finished":
                count += 1
                continue
            if current_turn == "X":
                queue.append((child_node, "O"))
            else:
                queue.append((child_node, "X"))
    return count


"""
Finds all distinct games
"""


def distinct_final_boards():
    queue = deque([(".........", "X")])
    final_boards = {"........."}
    count = 0
    while queue:
        current_board, current_turn = queue.popleft()
        for child_node in possible_moves(current_board, current_turn):
            if not goal_test(child_node) == "Not finished":
                if child_node not in final_boards:
                    count += 1
                    final_boards.add(child_node)
                continue
            if current_turn == "X":
                queue.append((child_node, "O"))
            else:
                queue.append((child_node, "X"))
    return count


"""
Finds all distinct final boards
"""


def distinct_final_boards_draw():
    queue = deque([(".........", "X")])
    final_boards = {"........."}
    count = 0
    while queue:
        current_board, current_turn = queue.popleft()
        for child_node in possible_moves(current_board, current_turn):
            if not goal_test(child_node) == "Not finished":
                if child_node not in final_boards:
                    if goal_test(child_node) == "Tie":
                        count += 1
                        final_boards.add(child_node)
                continue
            if current_turn == "X":
                queue.append((child_node, "O"))
            else:
                queue.append((child_node, "X"))
    return count


"""
Finds all distinct final boards that are draws
"""


def distinct_final_boards_X_wins(steps):
    queue = deque([(".........", "X", 0)])
    final_boards = {"........."}
    count = 0
    while queue:
        current_board, current_turn, step_count = queue.popleft()
        for child_node in possible_moves(current_board, current_turn):
            if not goal_test(child_node) == "Not finished":
                if child_node not in final_boards:
                    if goal_test(child_node) == "X wins" and step_count + 1 == steps:
                        count += 1
                        final_boards.add(child_node)
                continue
            if current_turn == "X":
                queue.append((child_node, "O", step_count + 1))
            else:
                queue.append((child_node, "X", step_count + 1))
    return count


"""
Finds all distinct final boards in which X wins in a given number of steps
"""


def distinct_final_boards_O_wins(steps):
    queue = deque([(".........", "X", 0)])
    final_boards = {"........."}
    count = 0
    while queue:
        current_board, current_turn, step_count = queue.popleft()
        for child_node in possible_moves(current_board, current_turn):
            if not goal_test(child_node) == "Not finished":
                if child_node not in final_boards:
                    if goal_test(child_node) == "O wins" and step_count + 1 == steps:
                        count += 1
                        final_boards.add(child_node)
                continue
            if current_turn == "X":
                queue.append((child_node, "O", step_count + 1))
            else:
                queue.append((child_node, "X", step_count + 1))
    return count


"""
Finds all distinct final boards in which O wins in a given number of steps
"""


async def print_board(message, board):
    board_print = ''
    N = int(len(board) ** (1 / 2))
    for x in range(N):
        for y in range(N):
            board_print += board[x * N + y] + '  \t'
        board_print += '\n'
    await message.channel.send(board_print)


def distinct_wins_from_here(board, turn):
    queue = deque([(board, turn)])
    # final_boards = {board}
    count = 0
    while queue:
        current_board, current_turn = queue.popleft()
        for child_node in possible_moves(current_board, current_turn):
            if not goal_test(child_node) == "Not finished":
                if turn == "X" and goal_test(child_node) == "X wins" or turn == "O" and goal_test(
                        child_node) == "O wins":
                    count += 1
                continue
            if current_turn == "X":
                queue.append((child_node, "O"))
            else:
                queue.append((child_node, "X"))
    return count


async def run_game(message, client, board, turn):
    if turn == "O":
        await run_game_helper(message, client, board, "X", True)
    else:
        await run_game_helper(message, client, board, "X", False)


async def run_game_helper(message, client, board, turn, human):
    if goal_test(board) != "Not finished":
        await print_board(message, board)
        result = goal_test(board)
        if human and result == "%s wins" % turn:
            await message.channel.send("You win!")
        elif not human and result == "%s wins" % turn:
            await message.channel.send("I win!")
        else:
            await message.channel.send("Tie!")
        return
    while goal_test(board) == "Not finished":
        await message.channel.send("Current board:")
        await print_board(message, board)
        if human is True:
            available = list()
            for index, char in enumerate(board):
                if char == ".":
                    available.append(str(index))
            await message.channel.send("You can move to any of these spaces: %s." % ", ".join(available))

            def check(mess):
                if mess.author.id == message.author.id and mess.channel == message.channel:
                    if mess.content in available:
                        return True
                    else:
                        pass
                        # await mess.channel.send("Sorry, you must an available position!")
                return False

            try:
                await message.channel.send('Your choice?')
                msg = await client.wait_for("message", check=check, timeout=30)  # 30 seconds to reply
                choice = int(msg.content)
                board = board[:choice] + turn + board[choice + 1:]
                if turn == "X":
                    turn = "O"
                else:
                    turn = "X"
                human = False
            except asyncio.TimeoutError:
                await message.channel.send("Sorry, you didn't reply in time! Try c!tictactoe again!")
                return
        else:
            possible_set = possible_moves(board, turn)
            best = "None"
            processed = process_possible(possible_set, turn)
            old_board = board
            for possible, condition in processed:
                result = goal_test(possible)
                if result == "%s wins" % turn:
                    board = possible
                    break
                if condition == "W":
                    board = possible
                elif condition == "T" and best != "T" and best != "W":
                    best = "T"
                    board = possible
                elif condition == "L" and best == "None":
                    best = "L"
                    board = possible
            await message.channel.send(f'I choose to move to space {moved(old_board, board)}')
            if turn == "X":
                turn = "O"
            else:
                turn = "X"
            human = True
    await print_board(message, board)
    result = goal_test(board)
    if result == "Tie":
        await message.channel.send("Tie")
        return
    if human is False:
        if turn == "O":
            if result == "X wins":
                await message.channel.send("You win!")
                return
            else:
                await message.channel.send("I win!")
                return
        if turn == "X":
            if result == "O wins":
                await message.channel.send("You win!")
                return
            else:
                await message.channel.send("I win!")
                return
    if human:
        if turn == "O":
            if result == "X wins":
                await message.channel.send("I win!")
                return
            else:
                await message.channel.send("You win!")
                return
        if turn == "X":
            if result == "O wins":
                await message.channel.send("I win!")
                return
            else:
                await message.channel.send("You win!")
                return


def moved(old_board, new_board):
    for index, char in enumerate(new_board):
        if char != old_board[index]:
            return index
    return -1


def process_possible(possible_set, turn):
    result = set()
    for possible in possible_set:
        if turn == "X":
            val = maximize(possible)
            if val == 1:
                result.add((possible, "W"))
            elif val == 0:
                result.add((possible, "L"))
            else:
                result.add((possible, "T"))
        else:
            val = minimize(possible)
            if val == 1:
                result.add((possible, "L"))
            elif val == 0:
                result.add((possible, "W"))
            else:
                result.add((possible, "T"))
    return result


def maximize(board):
    turn = "X"
    result = evaluate_board(board)
    if result != -1:
        return result
    trying = set()
    for possible in possible_moves(board, turn):
        trying.add(minimize(possible))
    return min(trying)


def minimize(board):
    turn = "O"
    result = evaluate_board(board)
    if result != -1:
        return result
    trying = set()
    for possible in possible_moves(board, turn):
        trying.add(maximize(possible))
    return max(trying)


def evaluate_board(board):
    result = goal_test(board)
    if result != "Not finished":
        if result == "Tie":
            return .5
        if result == "X wins":
            return 1
        if result == "O wins":
            return 0
    return -1


"""
Runs the game method
"""
