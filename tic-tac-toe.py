def min_max(board: list[list[int]], should_maximize: bool = True, depth: int = 0):
    winner = check_winner(board, depth)
    if winner != 0:
        return {
            "score": winner,
            "row": -1,
            "col": -1
        }

    if is_end(board):
        return {
            "score": winner,
            "row": -1,
            "col": -1
        }

    best_direction = [-1, -1]
    best_direction_score = -20 if should_maximize else 20

    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                board[row][col] = 1 if should_maximize else -1
                result = min_max(board, should_maximize=not should_maximize, depth=depth + 1)
                board[row][col] = 0
                if is_first_better(result["score"], best_direction_score, should_maximize):
                    best_direction = [row, col]
                    best_direction_score = result["score"]

    return {
        "row": best_direction[0],
        "col": best_direction[1],
        "score": best_direction_score
    }


def is_first_better(first: int, second: int, should_maximize):
    if should_maximize:
        return first > second
    else:
        return first < second


def check_winner(board: list[list[int]], depth):
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


def is_end(board: list[list[int]]):
    return all(all(col != 0 for col in row) for row in board)


def solve_game(board: list[list[int]]):
    min_max(board)


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

    should_maximize = (player == "X")

    result = min_max(board, should_maximize=should_maximize, depth=0)
    print_move_from_minimax_result(result)


def main():
    mode = input().strip()
    if mode == "JUDGE":
        judge_mode()
    else:
        pass


if __name__ == "__main__":
    main()

