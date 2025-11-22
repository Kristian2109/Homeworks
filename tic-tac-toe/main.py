from minMax import MinMaxAlgorithm


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