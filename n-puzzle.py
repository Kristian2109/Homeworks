import sys
import math

sys.setrecursionlimit(10**7)

DIRECTIONS = [
    ("left", 0, 1),
    ("right", 0, -1),
    ("up", 1, 0),
    ("down", -1, 0)
]


class State():
    def __init__(self, board, zero_position):
        self.board: list[int] = board
        self.zero_position: int = zero_position


class IdaStar():
    def __init__(self, board: list[int], target: dict[int, int], size: int):
        self.initialState = State(board, board.index(0))
        self.size = size
        self.path = []
        self.target = target
        self.current_threshold = manhattan_distance(self.initialState, target, size)

    def execute(self):
        while True:
            print(f"Current threshold: {self.current_threshold}")
            result = self._search(self.initialState, None, 0)
            if result is True:
                return self.path
            
            if result == float("inf"):
                return None
            
            self.current_threshold = result

    def _search(self, node: State, prev_move_name: str, current_distance: int):
        estimated_distance = current_distance + manhattan_distance(node, self.target, self.size)

        if estimated_distance > self.current_threshold:
            return estimated_distance
        
        if estimated_distance == current_distance:
            return True
        
        min_cost = float("inf")
        zero_x, zero_y = divmod(node.zero_position, self.size)

        for (direction_name, dx, dy) in DIRECTIONS:
            if prev_move_name == "left" and direction_name == "right": continue
            if prev_move_name == "right" and direction_name == "left": continue
            if prev_move_name == "up" and direction_name == "down": continue
            if prev_move_name == "down" and direction_name == "up": continue

            new_x = zero_x + dx
            new_y = zero_y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                new_zero_index = new_x * self.size + new_y
                self.path.append(direction_name)
                new_board = list(node.board)
                new_board[node.zero_position], new_board[new_zero_index] = \
                    new_board[new_zero_index], new_board[node.zero_position]
                new_state = State(new_board, new_zero_index)

                result = self._search(new_state, direction_name, current_distance + 1)
                if result is True:
                    return True
                if result < min_cost:
                    min_cost = result
                
                self.path.pop()

        return min_cost
    
    def is_solvable(self):
        board = [x for x in self.initialState.board if x != 0]
        inv_count = 0
        target_zero_position = self.target[0]
        start_zero_position = self.initialState.board.index(0)

        for i in range(len(board)):
            for j in range(i + 1, len(board)):
                if board[i] > board[j]:
                    inv_count += 1

        if self.size % 2 == 1:
            return inv_count % 2 == 0
        else:
            start_zero_row = self.size - (start_zero_position // self.size)
            target_zero_row = self.size - (target_zero_position // self.size)
            if (inv_count + start_zero_row + target_zero_row) % 2 == 0:
                return True
            return False
        

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


def main():
    numbers_count = int(sys.stdin.readline().strip())
    target_zero_position = int(sys.stdin.readline().strip())
    board_size = int(math.sqrt(numbers_count + 1))
    board: list[int] = []

    for i in range(board_size):
        board.extend(list(map(int, sys.stdin.readline().split())))

    target_board: list[int] = []

    for i in range(1, board_size * board_size):
        target_board.append(i)
    target_board.append(0)

    if target_zero_position != -1:
        end_position = board_size * board_size
        for i in reversed(range(target_zero_position + 1, end_position)):
            target_board[i], target_board[i-1] = target_board[i-1], target_board[i]

    positions_by_node: dict[int, int] = {}
    for i in target_board:
        positions_by_node[target_board[i]] = i

    algorithm = IdaStar(board, positions_by_node, board_size)

    if not algorithm.is_solvable():
        print(-1)
        return
    
    result = algorithm.execute()
    print(len(result))
    for move in result:
        print(move)


if __name__ == "__main__":
    main()
