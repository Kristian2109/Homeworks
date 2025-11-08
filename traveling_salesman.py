import math
import random
import numpy
from random import uniform

POPULATION_SIZE = 10
PLANE_DIMENSION = 100
MAX_ITERATIONS = 10000


class Point:
    def __init__(self, index, x, y, name=""):
        self.index: int = index
        self.x: int = x
        self.y: int = y
        self.name: str = name


class TSP:
    def __init__(self, points: list[Point]):
        self.points: list[Point] = points
        self.points_count = len(points)
        self.distance_matrix: list[list[float]] = self.get_distance_matrix()

    def get_distance_matrix(self):
        distance_matrix = []
        points_count = len(self.points)
        for i in range(points_count):
            current_point = self.points[i]
            distance_matrix.append([])
            for j in range(points_count):
                target_point = self.points[j]
                current_distance = math.sqrt((current_point.x - target_point.x) ** 2 +
                                             (current_point.y - target_point.y) ** 2)
                distance_matrix[i].append(current_distance)

        return distance_matrix

    def find_best_path(self):
        population: list[list[int]] = []
        chromosome = [i for i in range(self.points_count)]
        for i in range(POPULATION_SIZE):
            random.shuffle(chromosome)
            population.append(chromosome.copy())

        population_scores: list[float] = []
        for (index, chromosome) in enumerate(population):
            population_scores.append(self.evaluate_path_score(chromosome))

        best_path_lens_per_iteration: list[float] = []
        while len(best_path_lens_per_iteration) < MAX_ITERATIONS:
            new_population: list[list[int]] = []
            first_part = POPULATION_SIZE // 10

            best_paths = self.elitism_selection(population, population_scores, first_part)
            new_population.extend(best_paths)

            roulette_wheel_selection = self.roulette_wheel_with_crossover(population, population_scores,
                                                                          POPULATION_SIZE - first_part)
            new_population.extend(roulette_wheel_selection)

            population_scores = [self.evaluate_path_score(path) for path in new_population]
            population = new_population

            self.mutate(population[first_part:])

            best_path_len = 100 / max(population_scores)
            best_path_lens_per_iteration.append(best_path_len)

        p = max(len(best_path_lens_per_iteration) // 20, 1)
        for (index, path) in enumerate(best_path_lens_per_iteration):
            if index % p == 0:
                print(f"{index}    -   {path}")

    def evaluate_path_score(self, path: list[int]):
        score = 0
        for i in range(self.points_count - 1):
            begin = path[i]
            end = path[i + 1]
            score += self.distance_matrix[begin][end]

        return 100 / score

    @classmethod
    def elitism_selection(cls, population: list[list[int]], population_scores: list[float], selections_count: int):
        order = numpy.array(sorted([*enumerate(population_scores)], key=lambda x: x[1], reverse=True), dtype=int)[:, 0]
        sorted_population = [population[i] for i in order]
        return [sorted_population[i] for i in range(selections_count)]

    @classmethod
    def roulette_wheel_with_crossover(cls, population: list[list[int]], population_scores: list[float], selections_count: int):
        res = []
        for i in range(selections_count):
            parent_indexes = random.choices(range(POPULATION_SIZE), weights=population_scores, k=2)
            first_parent = population[parent_indexes[0]]
            second_parent = population[parent_indexes[1]]
            res.append(partially_mapped_crossover(first_parent, second_parent))
        return res

    def mutate(self, population: list[list[int]]):
        for i in range(len(population)):
            if random.uniform(0, 1) > 0.9:
                [first, second] = random.choices(range(self.points_count), k=2)
                population[i][first], population[i][second] = population[i][second], population[i][first]


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

    alg = TSP(points)
    alg.find_best_path()


if __name__ == '__main__':
    main()