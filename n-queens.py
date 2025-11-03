import math
from random import uniform


def generate_random_int(upper_bound: int):
    return math.floor(uniform(0, upper_bound))


def main():
    queens_count: int = int(input())
    queens_positions = [1, 2, 2, 2]# [generate_random_int(queens_count) for _ in range(queens_count)]
    queens_per_row = [0] * queens_count
    queens_per_positive_diagonal = [0] * (2 * queens_count - 1)
    queens_per_negative_diagonal = [0] * (2 * queens_count - 1)

    for (col, row) in enumerate(queens_positions):
        queens_per_row[row] += 1
        queens_per_positive_diagonal[row + col] += 1
        queens_per_negative_diagonal[queens_count - 1 - row + col] += 1

    total_conflicts_count = 0
    total_conflicts_count += sum(math.comb(i, 2) for i in queens_per_row if i > 1)
    total_conflicts_count += sum(math.comb(i, 2) for i in queens_per_positive_diagonal if i > 1)
    total_conflicts_count += sum(math.comb(i, 2) for i in queens_per_negative_diagonal if i > 1)

    print(queens_positions)
    print(queens_per_row)
    print(queens_per_negative_diagonal)
    print(queens_per_positive_diagonal)
    print(total_conflicts_count)
    # while True:
    #



if __name__ == "__main__":
    main()
