import os
import random
import time
from typing import List, Union
import sys


def print_board(queens: List[int]) -> None:
    N = len(queens)
    for r in range(N):
        row = []
        for c in range(N):
            row.append('*' if queens[c] == r else '_')
        print(' '.join(row))


def total_conflicts_from_counts(row_counts, pos_counts, neg_counts):
    """Utility (not used in main loop) to compute total pair conflicts if needed."""
    from math import comb
    total = 0
    for v in row_counts:
        if v > 1:
            total += comb(v, 2)
    for v in pos_counts:
        if v > 1:
            total += comb(v, 2)
    for v in neg_counts:
        if v > 1:
            total += comb(v, 2)
    return total


def min_conflicts_n_queens(N: int,
                           max_steps: int = None,
                           print_solution: bool = True,
                           measure_time: bool = True) -> Union[List[int], int]:
    """
    Solve N-Queens using Min-Conflicts.

    Returns list of length N: index = column, value = row; or -1 if no solution (N in {2,3} or failed).
    """

    if N in (2, 3):
        return -1

    if max_steps is None:
        max_steps = 10 * N  # reasonable default; can be tuned

    start = time.perf_counter()

    # --- Initialization ---
    # A queen in every column; row chosen uniformly random from 0..N-1
    queens = [random.randint(0, N - 1) for _ in range(N)]

    # Counts
    row_counts = [0] * N
    pos_diag_counts = [0] * (2 * N - 1)   # index = row + col
    neg_diag_counts = [0] * (2 * N - 1)   # index = (N-1 - row) + col

    # Fill counts
    for col, row in enumerate(queens):
        row_counts[row] += 1
        pos_diag_counts[row + col] += 1
        neg_diag_counts[(N - 1 - row) + col] += 1

    # Helper to compute conflicts for a queen currently at (col, queens[col])
    def conflicts_of_column(col: int) -> int:
        row = queens[col]
        # each queen contributes +1 to its row, pos_diag and neg_diag counts;
        # subtract 3 to count only other queens that conflict with this one
        return (row_counts[row] + pos_diag_counts[row + col] + neg_diag_counts[(N - 1 - row) + col] - 3)

    # Build initial list (set) of conflicted columns
    conflicted = [c for c in range(N) if conflicts_of_column(c) > 0]

    # Main loop
    for step in range(max_steps):
        if not conflicted:
            # solved
            elapsed = time.perf_counter() - start
            if measure_time and os.environ.get("FMI_TIME_ONLY"):
                print(f"{elapsed * 1000:.0f}")
            return queens

        # pick random conflicted column
        col = random.choice(conflicted)
        old_row = queens[col]

        # Remove queen from counts temporarily
        row_counts[old_row] -= 1
        pos_diag_counts[old_row + col] -= 1
        neg_diag_counts[(N - 1 - old_row) + col] -= 1

        # Find row(s) with minimal conflicts for this column
        min_conf = None
        best_rows = []
        # Evaluate conflicts for every possible row in O(N) (standard min-conflicts)
        for r in range(N):
            conf = row_counts[r] + pos_diag_counts[r + col] + neg_diag_counts[(N - 1 - r) + col]
            # conf is number of other queens that would conflict if queen placed at (col, r)
            if (min_conf is None) or (conf < min_conf):
                min_conf = conf
                best_rows = [r]
            elif conf == min_conf:
                best_rows.append(r)

        # Choose randomly among best rows
        new_row = random.choice(best_rows)
        queens[col] = new_row

        # Put queen back into counts at new_row
        row_counts[new_row] += 1
        pos_diag_counts[new_row + col] += 1
        neg_diag_counts[(N - 1 - new_row) + col] += 1

        # Update conflicted list: only columns whose conflict status may have changed:
        # those columns that share row or diagonals with old_row or new_row
        # We'll rebuild the conflicted list incrementally by checking all affected columns.
        # To keep it simple and robust we will touch every column whose queen lies in:
        # row old_row, row new_row, pos diag old, pos diag new, neg diag old, neg diag new.
        # Build a boolean mask of possibly affected columns.
        affected_mask = [False] * N

        # mark columns in same row as old_row or new_row
        # Instead of scanning N for each, we will scan all columns but only mark those with matching indices.
        # This loop is O(N) but very cheap; alternative more complex structures can reduce it.
        # We'll optimize by checking membership using fast operations.
        for c in range(N):
            r = queens[c]
            # r is current row of queen at column c (after move)
            if r == old_row or r == new_row or (r + c == old_row + col) or (r + c == new_row + col) or ((N - 1 - r) + c == (N - 1 - old_row) + col) or ((N - 1 - r) + c == (N - 1 - new_row) + col):
                affected_mask[c] = True

        # Rebuild conflicted list: update only affected columns, and keep others
        new_conflicted = []
        for c in range(N):
            if affected_mask[c]:
                # recompute conflict for this column
                conf = row_counts[queens[c]] + pos_diag_counts[queens[c] + c] + neg_diag_counts[(N - 1 - queens[c]) + c] - 3
                if conf > 0:
                    new_conflicted.append(c)
            else:
                # keep previous status if not affected
                # but we need to know previous membership; faster to recompute for all
                # to keep code simple and correct we recompute for all (still quite fast)
                conf = row_counts[queens[c]] + pos_diag_counts[queens[c] + c] + neg_diag_counts[(N - 1 - queens[c]) + c] - 3
                if conf > 0:
                    new_conflicted.append(c)

        conflicted = new_conflicted

    # if we get here, failed to find solution within max_steps
    elapsed = time.perf_counter() - start
    if measure_time:
        print(f"Failed to find solution in {max_steps} steps. Time: {elapsed:.6f} s")
    return -1


if __name__ == "__main__":
    # Read N from stdin
    try:
        N = int(sys.stdin.readline().strip())
    except Exception:
        print("Invalid input")
        sys.exit(1)

    # For automatic testing you can toggle:
    # - print_solution=False to avoid printing board for big N
    # - adjust max_steps if needed
    result = min_conflicts_n_queens(N, max_steps=5 * N, print_solution=True, measure_time=True)
    print(result)
