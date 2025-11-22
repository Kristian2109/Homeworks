import os
import time
from NQueens import  NQueens


def print_board(queens_rows: list[int]):
    n = len(queens_rows)
    for i in range(n):
        row = []
        for j in range(n):
            if queens_rows[j] == i:
                row.append("*")
            else:
                row.append("_")

        print("".join(row))


def main():
    is_for_time = os.environ.get("FMI_TIME_ONLY", False)
    queens_count: int = int(input())
    start = time.time()
    game = NQueens(queens_count)
    result = game.solve()

    if not is_for_time:
        print(result)
    else:
        total = time.time() - start
        print(f"# TIMES MS: alg={total * 1000:.0f}")


if __name__ == "__main__":
    main()