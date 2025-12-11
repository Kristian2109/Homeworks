from typing import Sequence
from math import sqrt


def euclidean_distance(first: Sequence, second: Sequence):
    seq_len = len(first)
    non_squared_distance: float = 0.
    for i in range(seq_len):
        non_squared_distance += (first[i] - second[i]) ** 2

    return sqrt(non_squared_distance)