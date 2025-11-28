from random import randint, sample


def partially_mapped_crossover(first: list[int], second: list[int]):
    size = len(first)
    a = randint(0, size - 1)
    b = randint(0, size - 1)

    lower_index = min(a, b)
    upper_index = max(a, b)
    print(f"Lower {lower_index} - Upper {upper_index}")

    mapping = {}
    for index in range(lower_index, upper_index):
        mapping[second[index]] = index

    result = [None] * size

    for i in range(size):
        if lower_index <= i < upper_index:
            result[i] = second[i]
            continue

        candidate = first[i]

        while candidate in mapping:
            opposing_index = mapping[candidate]
            candidate = first[opposing_index]

        result[i] = candidate

    return result


def n_points_crossover(first: list[int], second: list[int], points_count):
    size = len(first)
    points = [0] + sorted(sample(range(1, size), points_count)) + [size]

    result = [None] * size
    print(points)

    for i in range(len(points) - 1):
        add_from = first if i % 2 else second
        result[points[i]:points[i+1]] = add_from[points[i]:points[i+1]]

    return result


def main():
    p1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    p2 = [8, 7, 6, 5, 4, 3, 2, 1, 11, 10, 9]
    res = n_points_crossover(p1, p2, 4)
    print(res)


if __name__ == "__main__":
    main()