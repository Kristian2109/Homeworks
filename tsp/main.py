# import os
# import time
from typing import List
from random import uniform
from tsp_ga import TravelingSalesman, PLANE_DIMENSION, Point


def generate_random_points(points_count: int) -> List[Point]:
    return [Point(i, x=uniform(0, PLANE_DIMENSION), y=uniform(0, PLANE_DIMENSION)) for i in range(points_count)]


def get_points_from_console(n: int):
    points = []
    for i in range(n):
        point_info = input().split()
        new_point = Point(i, float(point_info[1]), float(point_info[2]), point_info[0])
        points.append(new_point)
    return points


def solution(points, are_cities: bool):
    # time_only = os.getenv("FMI_TIME_ONLY", "0") == "1"
    # bench_mode = "--bench" in os.sys.argv
    # start_time = time.perf_counter()
    alg = TravelingSalesman(points)
    best_path, best_path_len = alg.find_best_path()

    # elapsed_ms = (time.perf_counter() - start_time) * 1000
    #
    # if bench_mode or time_only:
    #     print(f"# TIMES_MS: alg={elapsed_ms:.2f}")
    #
    # if not time_only:
    print()
    start_in_best = best_path.index(0)
    result = []
    for i in range(start_in_best, len(points)):
        result.append(points[best_path[i]].name)
    for i in range(start_in_best):
        result.append(points[best_path[i]].name)

    if are_cities:
        print(" -> ".join(result))
    print(best_path_len)
    return best_path_len


def main():
    are_cities = False
    # start_time = time.perf_counter()

    n = input().strip()
    points: list[Point]
    if n.isdigit():
        n = int(n)
        points = generate_random_points(n)
    else:
        are_cities = True
        n = int(input())
        points = get_points_from_console(n)

    solution(points, are_cities)

    # results = []
    # for i in range(10):
    #     results.append(solution(points, are_cities))

    # elapsed_ms = (time.perf_counter() - start_time) * 1000
    # print(f"# TIMES_MS: alg={elapsed_ms:.2f}")
    # print(results)


if __name__ == '__main__':
    main()
