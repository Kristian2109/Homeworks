import math
from random import randint, choice


class NQueens:
    def __init__(self, n: int):
        self.n = n
        self.queens_rows = [randint(0, self.n - 1) for _ in range(self.n)]
        self.queens_per_row = [0] * self.n
        self.queens_per_positive_diagonal = [0] * (2 * self.n - 1)
        self.queens_per_negative_diagonal = [0] * (2 * self.n - 1)
        self.total_conflicts_count = 0

        for (col, row) in enumerate(self.queens_rows):
            self.queens_per_row[row] += 1
            self.queens_per_positive_diagonal[row + col] += 1
            self.queens_per_negative_diagonal[self.n - 1 - row + col] += 1

        self.total_conflicts_count += sum(math.comb(i, 2) for i in self.queens_per_row if i > 1)
        self.total_conflicts_count += sum(math.comb(i, 2) for i in self.queens_per_positive_diagonal if i > 1)
        self.total_conflicts_count += sum(math.comb(i, 2) for i in self.queens_per_negative_diagonal if i > 1)

    def solve(self):
        if self.n == 2 or self.n == 3:
            return -1

        outstanding_iterations = self.n * max(20, 120 - self.n)

        while outstanding_iterations > 0:
            if self.total_conflicts_count == 0:
                return self.queens_rows

            col = randint(0, self.n - 1)
            old_row = self.queens_rows[col]
            if self.queens_per_row[old_row] <= 1 and \
                    self.queens_per_positive_diagonal[old_row + col] <= 1 and \
                    self.queens_per_negative_diagonal[self.n - 1 - old_row + col] <= 1:
                continue

            self.queens_per_row[old_row] -= 1
            self.queens_per_positive_diagonal[col + old_row] -= 1
            self.queens_per_negative_diagonal[self.n - 1 - old_row + col] -= 1

            best_rows = self.get_min_conflicted_rows(col)
            new_row = choice(best_rows)

            self.total_conflicts_count -= self.get_conflicts_count(col, old_row)
            self.total_conflicts_count += self.get_conflicts_count(col, new_row)
            self.queens_rows[col] = new_row

            self.queens_per_row[new_row] += 1
            self.queens_per_positive_diagonal[col + new_row] += 1
            self.queens_per_negative_diagonal[self.n - 1 - new_row + col] += 1

            outstanding_iterations -= 1

        return -1

    def get_min_conflicted_rows(self, col) -> list[int]:
        min_conflicts = self.get_conflicts_count(col, self.queens_rows[col])
        min_rows = [self.queens_rows[col]]

        for row in range(self.n):
            if row == self.queens_rows[col]:
                continue

            current_conflicts = self.get_conflicts_count(col, row)
            if current_conflicts < min_conflicts:
                min_rows = [row]
                min_conflicts = current_conflicts
            elif current_conflicts == min_conflicts:
                min_rows.append(row)

        return min_rows

    def get_conflicts_count(self, col, row):
        return self.queens_per_row[row] + \
               self.queens_per_positive_diagonal[row + col] + \
               self.queens_per_negative_diagonal[self.n - 1 - row + col]

