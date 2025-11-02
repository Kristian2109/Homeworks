import sys
import math

sys.setrecursionlimit(10**7)

# Directions: (name, dx, dy)
DIRECTIONS = [
    ("left", 0, 1),
    ("right", 0, -1),
    ("up", 1, 0),
    ("down", -1, 0)
]

class State():
    def __init__(self, board):
        self.board: list[int] = board


def ida_star(initial: State, target: dict[int, int], size: int):
    current_threshold = manhattan_distance(initial, target, size)
    path = []

    while True:
        result = search(initial, initial.board.index(0), target, None, 0, current_threshold, path, size)
        if result is True:
            return path
        
        if result == float("inf"):
            return None
        
        current_threshold = result

def search(node: State, null_index: int, target: dict[int, int], prev_move: str, current_distance: int, threshold: int, path: list[str], size: int):
    estimated_distance = current_distance + manhattan_distance(node, target, size)

    if estimated_distance > threshold:
        return estimated_distance
    
    if estimated_distance == current_distance:
        return True
    
    min_cost = float("inf")
    zero_x, zero_y = divmod(null_index, size)

    for (name, dx, dy) in DIRECTIONS:
        if prev_move == "left" and name == "right": continue
        if prev_move == "right" and name == "left": continue
        if prev_move == "up" and name == "down": continue
        if prev_move == "down" and name == "up": continue

        new_x = zero_x + dx
        new_y = zero_y + dy
        if 0 <= new_x < size and 0 <= new_y < size:
            new_zero_index = new_x * size + new_y
            path.append(name)
            new_board = list(node.board)
            new_board[null_index], new_board[new_zero_index] = new_board[new_zero_index], new_board[null_index]
            new_state = State(new_board)

            result = search(new_state, new_zero_index, target, name, current_distance + 1, threshold, path, size)
            if result is True:
                return True
            if result < min_cost:
                min_cost = result
            
            path.pop()

    return min_cost


def manhattan_distance(current: State, target: dict[int, int], size):
    dist = 0
    for i in range(size * size):
        current_node = current.board[i]
        if current_node == 0:
            continue
        current_x, current_y = divmod(i, size)
        target_x, target_y = divmod(target[current_node], size)
        dist += abs(target_x - current_x)
        dist += abs(target_y - current_y)
    
    return dist

def is_solvable(board, size, zero_pos_goal):
    arr = [x for x in board if x != 0]
    inv_count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv_count += 1

    if size % 2 == 1:
        return inv_count % 2 == 0
    else:
        start_zero_row = size - (board.index(0) // size)
        goal_zero_row = size - (zero_pos_goal // size)
        if (inv_count + start_zero_row + goal_zero_row) % 2 == 0:
            return True
        return False


def main():
    numbers_count = int(sys.stdin.readline().strip())
    target_null_position = int(sys.stdin.readline().strip())

    board_size = int(math.sqrt(numbers_count + 1))
    board: list[int] = []

    for i in range(board_size):
        board.extend(list(map(int, sys.stdin.readline().split())))

    target_board: list[int] = []

    for i in range(1, board_size * board_size):
        target_board.append(i)
    target_board.append(0)

    if target_null_position != -1:
        end_position = board_size * board_size
        for i in reversed(range(target_null_position + 1, end_position)):
            target_board[i], target_board[i-1] = target_board[i-1], target_board[i]

    positions_by_node: dict[int, int] = {}
    for i in target_board:
        positions_by_node[target_board[i]] = i
    # for i in range(board_size * board_size):
    #     print(target_board[i])


    if not is_solvable(board, board_size, target_null_position):
        print(-1)
        return
    
    initialState = State(board)
    result = ida_star(initialState, positions_by_node, board_size)
    print(len(result))
    for move in result:
        print(move)



if __name__ == "__main__":
    main()
