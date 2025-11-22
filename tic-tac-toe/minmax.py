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