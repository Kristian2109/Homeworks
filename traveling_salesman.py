# Python3 program to create target string, starting from
# random string using Genetic Algorithm
import math
import random
import numpy
from random import uniform

# Number of individuals in each generation
POPULATION_SIZE = 10
PLANE_DIMENSION = 100


class Point:
    def __init__(self, index, x, y):
        self.index: int = index
        self.x: int = x
        self.y: int = y


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


def main():
    N = int(input())
    points: list[Point] = []
    for i in range(N):
        points.append(Point(i, uniform(0, PLANE_DIMENSION), uniform(0, PLANE_DIMENSION)))

    # print(list(map(lambda el: {"x": el.x, "y": el.y}, points)))

    distance_matrix: list[list[float]] = []
    for i in range(N):
        current_point = points[i]
        distance_matrix.append([])
        for j in range(N):
            target_point = points[j]
            current_distance = math.sqrt((current_point.x - target_point.x) ** 2 +
                                         (current_point.y - target_point.y) ** 2)
            distance_matrix[i].append(current_distance)
        # print(distance_matrix[i])

    population: list[list[int]] = []
    chromosome = [i for i in range(N)]
    for i in range(POPULATION_SIZE):
        random.shuffle(chromosome)
        population.append(chromosome.copy())

    population_scores: list[float] = []
    for (index, chromosome) in enumerate(population):
        population_scores.append(evaluate_fitness_score(N, distance_matrix, chromosome))

    iteration = 0
    while iteration < 1000:
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
                [first, second] = random.choices(range(N), k=2)
                new_population[i][first], new_population[i][second] = new_population[i][second], new_population[i][first]

        population_scores = [evaluate_fitness_score(N, distance_matrix, path) for path in new_population]
        population = new_population

        print(f"Current best: {100 / max(population_scores)}")
        iteration += 1


if __name__ == '__main__':
    main()