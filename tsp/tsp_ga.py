import math
import random
import numpy

POPULATION_SIZE = 10
PLANE_DIMENSION = 500
MAX_ITERATIONS = 10000
ELITISM_SELECTION = 10
MUTATION_BY_INSERTION = 0.9
MUTATION_BY_SWAP = 0.8


class Point:
    def __init__(self, index, x, y, name=""):
        self.index: int = index
        self.x: int = x
        self.y: int = y
        self.name: str = name


class TravellingSalesman:
    def __init__(self, points: list[Point]):
        self.points: list[Point] = points
        self.points_count = len(points)
        self.distance_matrix: list[list[float]] = self.get_distance_matrix()

    def find_best_path(self) -> (list[int], float):
        population: list[list[int]] = []
        chromosome = [i for i in range(self.points_count)]
        for i in range(POPULATION_SIZE):
            random.shuffle(chromosome)
            population.append(chromosome.copy())

        scores: list[float] = []
        for (index, chromosome) in enumerate(population):
            scores.append(self.evaluate_path_score(chromosome))

        best_path_lens_per_iteration: list[float] = []
        iterations_count = 0
        completed_paths: list[list[int]] = []
        completed_paths_scores: list[float] = []

        while iterations_count < MAX_ITERATIONS:
            new_population: list[list[int]] = []
            first_part = POPULATION_SIZE // ELITISM_SELECTION

            best_paths = self.elitism_selection(population, scores, first_part)
            new_population.extend(best_paths)

            second_selection = self.roulette_wheel_with_crossover(population, scores, POPULATION_SIZE - first_part)
            new_population.extend(second_selection)

            self.mutate_by_insertion(new_population[first_part:])
            self.mutate_by_swap(new_population[first_part:])

            scores = [self.evaluate_path_score(path) for path in new_population]
            population = new_population

            best_path_len = 1 / max(scores)
            best_path_lens_per_iteration.append(best_path_len)

            if iterations_count > 1000 and \
                    best_path_lens_per_iteration[iterations_count - 1] == \
                    best_path_lens_per_iteration[iterations_count - 1000]:
                best_path_index = numpy.argmax(scores)
                completed_paths.append(population[best_path_index])
                population = []
                completed_paths_scores.append(max(scores))
                for i in range(POPULATION_SIZE):
                    random.shuffle(chromosome)
                    population.append(chromosome.copy())
                scores = [self.evaluate_path_score(path) for path in population]

            iterations_count += 1

        p = max(len(best_path_lens_per_iteration) // 11, 1)
        for (index, path) in enumerate(best_path_lens_per_iteration):
            if index % p == 0:
                print(path)

        if len(completed_paths) != 0:
            best_path_index = numpy.argmax(completed_paths_scores)
            return completed_paths[best_path_index], min(best_path_lens_per_iteration)

        best_path_index = numpy.argmax(scores)
        return population[best_path_index], min(best_path_lens_per_iteration)

    def evaluate_path_score(self, path: list[int]):
        score = 0
        for i in range(self.points_count - 1):
            begin = path[i]
            end = path[i + 1]
            score += self.distance_matrix[begin][end]
        return 1 / score

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
            res.append(cls.order_crossover(first_parent, second_parent))
        return res

    def mutate_by_swap(self, population: list[list[int]]):
        for i in range(len(population)):
            if random.uniform(0, 1) > MUTATION_BY_SWAP:
                [first, second] = random.choices(range(self.points_count), k=2)
                population[i][first], population[i][second] = population[i][second], population[i][first]

    def mutate_by_insertion(self, population: list[list[int]]):
        for i in range(len(population)):
            if random.uniform(0, 1) > MUTATION_BY_INSERTION:
                [first, second] = random.choices(range(self.points_count), k=2)
                current = population[i][first]
                population[i].pop(first)
                population[i].insert(second, current)

    @classmethod
    def partially_mapped_crossover(cls, parent1: list[int], parent2: list[int]) -> list[int]:
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

    @classmethod
    def order_crossover(cls, parent1: list[int], parent2: list[int]) -> list[int]:
        size = len(parent1)
        p1, p2 = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[p1:p2 + 1] = parent1[p1:p2 + 1]
        pos = (p2 + 1) % size
        for gene in parent2:
            if gene not in child:
                child[pos] = gene
                pos = (pos + 1) % size
        return child

    def get_distance_matrix(self):
        distance_matrix = []
        points_count = len(self.points)
        for i in range(points_count):
            current_point = self.points[i]
            distance_matrix.append([])
            for j in range(points_count):
                target_point = self.points[j]
                current_distance = math.sqrt(
                    (current_point.x - target_point.x) ** 2 +
                    (current_point.y - target_point.y) ** 2
                )
                distance_matrix[i].append(current_distance)
        return distance_matrix