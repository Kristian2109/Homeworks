from typing import Dict, Set, Tuple
import heapq
import itertools
from sys import maxsize

counter = itertools.count()


class Node:
    def __init__(self, id_number: int, estimated_distance: int):
        self.id = id_number
        self.estimated_distance: int = estimated_distance
        self.children: list[int] = []
        self.children_distances: list[int] = []


NodesMap = Dict[int, Node]
DistancesMap = Dict[int, int]
NodesInheritance = Dict[int, int]


def get_path(end, came_from: NodesInheritance):
    result = [end]
    current = end
    while current in came_from:
        current = came_from[current]
        result.append(current)

    result.reverse()
    return result


def main():
    nodes_count: int = int(input())
    nodes: NodesMap = {}

    for _ in range(nodes_count):
        node_id = int(input())
        nodes[node_id] = Node(node_id)

    edges_count: int = int(input())
    for _ in range(edges_count):
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
    nodes_inheritance: Dict[int, int] = {}

    heapq.heappush(pq, (0, next(counter), nodes[start]))
    distances[start] = 0

    while len(pq) > 0:
        current_distance, _, current_node = heapq.heappop(pq)
        passed_nodes.add(current_node.id)
        if current_node.id == end:
            print(current_distance)
            break

        if distances[current_node.id] < current_distance:
            continue

        for child_index, child_id in enumerate(current_node.children):
            current_gone_distance = current_distance + current_node.children_distances[child_index]

            if distances.get(child_id, maxsize) > current_gone_distance:
                nodes_inheritance[child_id] = current_node.id
                new_estimated_distance = current_gone_distance + nodes[child_id].estimated_distance

                heapq.heappush(pq, (new_estimated_distance, next(counter), nodes[child_id]))
                distances[child_id] = current_gone_distance

    for node in distances.keys():
        print(f"Node {node} - Distance {distances[node]}")


if __name__ == '__main__':
    main()
