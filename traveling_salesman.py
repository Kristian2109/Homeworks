# Python3 program to create target string, starting from
# random string using Genetic Algorithm
import math
import random
import numpy
from random import uniform

# Number of individuals in each generation
POPULATION_SIZE = 10
PLANE_DIMENSION = 100
MAX_ITERATIONS = 10


class Point:
    def __init__(self, index, x, y, name=""):
        self.index: int = index
        self.x: int = x
        self.y: int = y
        self.name: str = name


class TSP:
    def __init__(self):
        self.distance_matrix: list[list[float]] = []


def partially_mapped_crossover(parent1, parent2) -> list[int]:
    size = len(parent1)
    p1, p2 = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[p1:p2 + 1] = parent2[p1:p2 + 1]
    mapping = {parent2[i]: parent1[i] for i in range(p1, p2 + 1)}

    for i in range(size):
        if i < p1 or i > p2:
            candidate = parent1[i]
            while candidate in child:
                candidate = mapping.get(candidate, candidate)
            child[i] = candidate

    return child


def evaluate_fitness_score(n: int, distance_matrix: list[list[float]], chromosome: list[int]):
    score = 0
    for i in range(n - 1):
        begin = chromosome[i]
        end = chromosome[i + 1]
        score += distance_matrix[begin][end]

    return 100 / score


def generate_random_points(points_count: int) -> list[Point]:
    return [Point(i, x=uniform(0, PLANE_DIMENSION), y=uniform(0, PLANE_DIMENSION)) for i in range(points_count)]


def get_points_from_console(n: int):
    points = []
    for i in range(n):
        point_info = input().split(" ")
        new_point = Point(i, float(point_info[1]), float(point_info[2]), point_info[0])
        points.append(new_point)
    return points


def main():
    n = input()
    points: list[Point]
    if n.isdigit():
        n = int(n)
        points = generate_random_points(n)
    else:
        n = int(input())
        points = get_points_from_console(n)

    # print(list(map(lambda el: {"x": el.x, "y": el.y}, points)))

    distance_matrix: list[list[float]] = []
    for i in range(n):
        current_point = points[i]
        distance_matrix.append([])
        for j in range(n):
            target_point = points[j]
            current_distance = math.sqrt((current_point.x - target_point.x) ** 2 +
                                         (current_point.y - target_point.y) ** 2)
            distance_matrix[i].append(current_distance)
        # print(distance_matrix[i])

    population: list[list[int]] = []
    chromosome = [i for i in range(n)]
    for i in range(POPULATION_SIZE):
        random.shuffle(chromosome)
        population.append(chromosome.copy())

    population_scores: list[float] = []
    for (index, chromosome) in enumerate(population):
        population_scores.append(evaluate_fitness_score(n, distance_matrix, chromosome))

    best_path_lens_per_iteration: list[float] = []
    while len(best_path_lens_per_iteration) < MAX_ITERATIONS:
        new_population: list[list[int]] = []
        order = numpy.array(sorted([*enumerate(population_scores)], key=lambda x: x[1], reverse=True), dtype=int)[:, 0]
        sorted_population = [population[i] for i in order]
        first_part = POPULATION_SIZE // 10
        for i in range(first_part):
            new_population.append(sorted_population[i])

        for i in range(first_part, POPULATION_SIZE):
            parents = random.choices(range(POPULATION_SIZE), weights=population_scores, k=2)
            new_population.append(partially_mapped_crossover(population[parents[0]], population[parents[1]]))

        for i in range(POPULATION_SIZE):
            if random.uniform(0, 1) > 0.9:
                [first, second] = random.choices(range(n), k=2)
                new_population[i][first], new_population[i][second] = new_population[i][second], new_population[i][first]

        population_scores = [evaluate_fitness_score(n, distance_matrix, path) for path in new_population]
        population = new_population

        best_path_len = 100 / max(population_scores)
        best_path_lens_per_iteration.append(best_path_len)

    for path in best_path_lens_per_iteration:
        print(path)


if __name__ == '__main__':
    main()