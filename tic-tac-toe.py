from typing import TypedDict


class Score(TypedDict):
    winner: int
    depth: int


def min_max(board: list[list[int]], should_maximize: bool = True, is_x: bool = True, depth: int = 0):
    best_direction = [-1, -1]
    best_direction_score = Score(winner=-10_000 if should_maximize else 10_000, depth=depth)

    winner = check_winner(board)
    if winner != 0:
        return {
            "score": Score(winner=winner, depth=depth),
            "row": -1,
            "col": -1
        }

    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                board[row][col] = 1 if is_x else -1
                result = min_max(board, should_maximize=not should_maximize, is_x=not is_x, depth=depth + 1)
                board[row][col] = 0
                if is_first_better(result["score"], best_direction_score, should_maximize):
                    best_direction = [row, col]
                    best_direction_score = result["score"]

    return {
        "row": best_direction[0],
        "col": best_direction[1],
        "score": Score(winner=0, depth=depth)
    }


def is_first_better(first: Score, second: Score, should_maximize):
    if should_maximize:
        return first["winner"] > second["winner"] or \
               first["winner"] == second["winner"] and first["depth"] < second["depth"]
    else:
        return first["winner"] < second["winner"] or \
            first["winner"] == second["winner"] and first["depth"] > second["depth"]


def check_winner(board: list[list[int]]):
    for row in range(3):
        if board[row][0] != 0 and all(col == board[row][0] for col in board[row]):
            return board[row][0]

    for col in range(3):
        if board[0][col] != 0 and all(row == board[0][col] for row in board[col]):
            return board[0][col]

    if all(board[diag][diag] == board[0][0] for diag in range(0, 3)):
        return board[0][0]

    if all(board[diag][2 - diag] == board[0][2] for diag in range(0, 3)):
        return board[0][2]

    return 0


def solve_game(board: list[list[int]]):
    min_max(board)


def main():
    board: list[list[int]] = [
        [1, 1, -1],
        [-1, -1, 0],
        [0, 0, 0]
    ]
    result = min_max(board, is_x=False)
    print(result)


if __name__ == "__main__":
    main()
