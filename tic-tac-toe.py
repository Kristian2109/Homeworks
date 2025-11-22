from typing import TypedDict


Board = list[list[int]]


class MixMaxResult(TypedDict):
    score: int
    row: int
    col: int


class MinMaxAlgorithm:
    def __init__(self, board: Board, is_x_bot: bool):
        self.board: Board = board
        self.is_x_bot: bool = is_x_bot

    def get_best_move(self):
        return self.min_max(should_maximize=self.is_x_bot)

    def min_max(self, should_maximize: bool, depth: int = 0, alpha: int = -100, beta: int = 100) -> MixMaxResult:
        winner = self.check_winner(depth)
        if winner != 0:
            return {
                "score": winner,
                "row": -1,
                "col": -1
            }

        if self.is_end():
            return {
                "score": winner,
                "row": -1,
                "col": -1
            }

        best_direction = [-1, -1]
        best_direction_score = -20 if should_maximize else 20

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    self.board[row][col] = 1 if should_maximize else -1
                    result = self.min_max(should_maximize=not should_maximize, depth=depth + 1, alpha=alpha, beta=beta)
                    self.board[row][col] = 0
                    if self.is_first_better(result["score"], best_direction_score, should_maximize):
                        best_direction = [row, col]
                        best_direction_score = result["score"]

                    alpha = max(result["score"], alpha) if should_maximize else alpha
                    beta = beta if should_maximize else min(result["score"], beta)
                    if beta <= alpha:
                        break

        return {
            "row": best_direction[0],
            "col": best_direction[1],
            "score": best_direction_score
        }

    @staticmethod
    def is_first_better(first: int, second: int, should_maximize: bool):
        return first > second if should_maximize else first < second

    def check_winner(self, depth):
        board = self.board

        for row in range(3):
            if board[row][0] != 0 and all(col == board[row][0] for col in board[row]):
                return board[row][0] * 10 - depth * board[row][0]

        for col in range(3):
            if board[0][col] != 0 and all(board[row][col] == board[0][col] for row in range(3)):
                return board[0][col] * 10 - depth * board[0][col]

        if board[0][0] != 0 and all(board[diag][diag] == board[0][0] for diag in range(0, 3)):
            return board[0][0] * 10 - depth * board[0][0]

        if board[2][2] != 0 and all(board[diag][2 - diag] == board[0][2] for diag in range(0, 3)):
            return board[0][2] * 10 - - depth * board[0][2]

        return 0

    def is_end(self):
        return all(all(col != 0 for col in row) for row in self.board)


def read_board_framed():
    board = []
    input()
    for _ in range(3):
        line = input().strip()
        parts = line.split("|")
        row = []
        for cell in parts[1:4]:
            symbol = cell.strip()
            if symbol == "X":
                row.append(1)
            elif symbol == "O":
                row.append(-1)
            else:
                row.append(0)
        board.append(row)
        input()
    return board


def print_move_from_minimax_result(result):
    r = result["row"]
    c = result["col"]
    if r == -1 and c == -1:
        print(-1)
    else:
        print(r + 1, c + 1)


def judge_mode():
    turn_line = input().strip()
    _, player = turn_line.split()

    board = read_board_framed()

    is_x_bot = (player == "X")

    min_max = MinMaxAlgorithm(board, is_x_bot)
    result = min_max.get_best_move()
    print_move_from_minimax_result(result)


def print_board(board: list[list[int]]):
    def sym(v):
        if v == 1:
            return "X"
        elif v == -1:
            return "O"
        else:
            return "_"

    print("+---+---+---+")
    for r in range(3):
        print(f"| {sym(board[r][0])} | {sym(board[r][1])} | {sym(board[r][2])} |")
        print("+---+---+---+")


def read_non_empty():
    line = input().strip()
    while line == "":
        line = input().strip()
    return line


def game_mode():
    input_for_first = read_non_empty()
    input_for_x = read_non_empty()
    is_x_first = input_for_first.split()[1].lower() == "x"
    is_x_human = input_for_x.split()[1].lower() == "x"

    board = read_board_framed()

    algorithm = MinMaxAlgorithm(board, is_x_bot=not is_x_human)

    is_human_turn = (is_x_human and is_x_first) or (not is_x_human and not is_x_first)
    human_number = 1 if is_x_human else -1

    while not algorithm.is_end():
        print_board(board)
        if is_human_turn:
            human_input = read_non_empty()
            row, col = map(int, human_input.split())
            if 1 <= row <= 3 and 1 <= col <= 3 and board[row - 1][col - 1] == 0:
                board[row - 1][col - 1] = human_number
        else:
            result = algorithm.get_best_move()
            r = result["row"]
            c = result["col"]
            board[r][c] = -1 if human_number == 1 else 1

        is_human_turn = not is_human_turn


def main():
    mode = input().strip()
    if mode.upper() == "JUDGE":
        judge_mode()
    else:
        game_mode()
        pass


if __name__ == "__main__":
    main()
