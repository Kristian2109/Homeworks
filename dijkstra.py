from typing import Dict, Set, Tuple
import heapq, itertools
from sys import maxsize
import itertools
counter = itertools.count()


class Node:
    def __init__(self, id_number: int, cost: int):
        self.id = id_number
        self.cost = cost
        self.children: list[int] = []
        self.children_distances: list[int] = []


NodesMap = Dict[int, Node]
DistancesMap = Dict[int, int]


def main():
    nodes_count: int = int(input())
    nodes: NodesMap = {}

    for i in range(nodes_count):
        cost = int(input())
        nodes[i + 1] = Node(i + 1, cost)

    edges_count: int = int(input())
    for i in range(edges_count):
        inp = input().split()
        first = int(inp[0])
        second = int(inp[1])
        distance = int(inp[2])

        parent: Node = nodes[first]
        parent.children.append(second)
        parent.children_distances.append(distance)

    start = int(input())
    end = int(input())

    pq: list[Tuple[int, int, Node]] = []
    passed_nodes: Set[int] = set()
    distances: DistancesMap = {}

    heapq.heappush(pq, (0, next(counter), nodes[start]))
    passed_nodes.add(start)

    while len(pq) > 0:
        current_distance, _, current_node = heapq.heappop(pq)
        passed_nodes.add(current_node.id)
        if current_node == end:
            break

        for child_index, child_id in enumerate(current_node.children):
            if child_id in passed_nodes:
                continue

            current_distance_to_child = current_node.children_distances[child_index] + current_distance
            distances[child_id] = min(current_distance_to_child, distances.get(child_id, maxsize))
            heapq.heappush(pq, (current_distance_to_child, next(counter), nodes[child_id]))

    for node in distances.keys():
        print(f"Node {node} - Distance {distances[node]}")


if __name__ == '__main__':
    main()
