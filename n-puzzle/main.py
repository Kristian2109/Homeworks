import sys
import math
from idaStart import IdaStar

sys.setrecursionlimit(10**7)


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
            target_board[i], target_board[i - 1] = target_board[i - 1], target_board[i]

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
