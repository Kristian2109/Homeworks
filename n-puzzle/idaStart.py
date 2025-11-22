class State:
    def __init__(self, board, zero_position):
        self.board: list[int] = board
        self.zero_position: int = zero_position


class IdaStar:
    DIRECTIONS = [
        ("left", 0, 1),
        ("right", 0, -1),
        ("up", 1, 0),
        ("down", -1, 0)
    ]

    def __init__(self, board: list[int], target: dict[int, int], size: int):
        self.initialState = State(board, board.index(0))
        self.size = size
        self.path = []
        self.target = target
        self.current_threshold = self.manhattan_distance(self.initialState, target, size)

    def execute(self):
        while True:
            result = self._search(self.initialState, "no_move", 0)
            if result is True:
                return self.path

            if result == float("inf"):
                return None

            self.current_threshold = result

    def _search(self, node: State, prev_move_name: str, current_distance: int):
        estimated_distance = current_distance + self.manhattan_distance(node, self.target, self.size)

        if estimated_distance > self.current_threshold:
            return estimated_distance

        if estimated_distance == current_distance:
            return True

        min_cost = float("inf")
        zero_x, zero_y = divmod(node.zero_position, self.size)

        for (direction_name, dx, dy) in self.DIRECTIONS:
            if prev_move_name == "left" and direction_name == "right": continue
            if prev_move_name == "right" and direction_name == "left": continue
            if prev_move_name == "up" and direction_name == "down": continue
            if prev_move_name == "down" and direction_name == "up": continue

            new_x = zero_x + dx
            new_y = zero_y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                self.path.append(direction_name)

                new_zero_index = new_x * self.size + new_y
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

    @classmethod
    def manhattan_distance(cls, current: State, target: dict[int, int], size):
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
