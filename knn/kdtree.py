import heapq
from itertools import count
from typing import Sequence, Tuple
from common import euclidean_distance

DIMENSIONALITY = 4


class Node:
    def __init__(self, left, right, point, cluster):
        self.left: Node = left
        self.right: Node = right
        self.point: list[float] = point
        self.cluster: int = cluster


def insert_point(node: Node, point: list[float], cluster: int, depth: int):
    if node is None:
        return Node(None, None, point, cluster)

    attribute_index = depth % DIMENSIONALITY

    if point[attribute_index] > node.point[attribute_index]:
        node.right = insert_point(node.right, point, cluster, depth + 1)
    else:
        node.left = insert_point(node.left, point, cluster, depth + 1)

    return node


def build_tree(points_with_clusters: Sequence[Sequence]):
    root = None
    for point in points_with_clusters:
        root = insert_point(root, point[:-1], point[-1], 0)

    return root


counter = count()


def search_nearest_neighbors(current_node: Node, point: Sequence[float], heap: list[Tuple[float, int, Node]], depth: int, k: int):
    if current_node is None:
        return

    attribute_index = depth % DIMENSIONALITY
    current_dist = euclidean_distance(current_node.point, point)

    if len(heap) < k:
        heapq.heappush(heap, (-current_dist, next(counter), current_node))
    else:
        current_worst, _, _ = heapq.nsmallest(1, heap)[0]
        if current_worst < -current_dist:
            heapq.heappop(heap)
            heapq.heappush(heap, (-current_dist, next(counter), current_node))

    if point[attribute_index] > current_node.point[attribute_index]:
        better_branch = current_node.right
        worse_branch = current_node.left
    else:
        better_branch = current_node.left
        worse_branch = current_node.right

    if not better_branch:
        better_branch, worse_branch = worse_branch, better_branch

    search_nearest_neighbors(better_branch, point, heap, depth + 1, k)

    worst_acceptable_distance = -10000000
    if len(heap) == k:
        worst_acceptable_distance, _, _ = heapq.nsmallest(1, heap)[0]

    dist_to_plane = -abs(current_node.point[attribute_index] - point[attribute_index])

    if dist_to_plane > worst_acceptable_distance:
        search_nearest_neighbors(worse_branch, point, heap, depth + 1, k)
