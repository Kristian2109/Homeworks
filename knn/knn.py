from typing import Sequence, Tuple
from kdtree import build_tree, Node, search_nearest_neighbors
from common import compute_accuracy
from random import shuffle
from statistics import mean, stdev


def knn(tree: Node, point: Sequence, k: int):
    best_nodes: list[Tuple[float, int, Node]] = []
    search_nearest_neighbors(tree, point[:-1], best_nodes, 0, k)

    best_k = [(-value[0], value[2].cluster) for value in sorted(best_nodes, key=lambda value: value[0], reverse=True)]
    values_count = [0] * 10

    for v in best_k:
        values_count[v[1]] += 1

    best = -10000000
    best_index = -100000
    for index, value_count in enumerate(values_count):
        if best < value_count:
            best_index = index
            best = value_count

    return {
        "best_cluster": best_index,
        "actual_cluster": point[-1],
        "best_k": best_k
    }


def predict_results(train, test, k):
    tree = build_tree(train)
    results = []
    for r in test:
        result = knn(tree, r, k)
        results.append(result)

    accuracy = compute_accuracy(results)
    return accuracy


def cross_fold_validation(dataset, clusters_count):
    shuffled_dataset = list(dataset)
    shuffle(shuffled_dataset)

    accuracies: list[float] = []
    for fold_number in range(10):
        test_dataset = dataset[fold_number * 15:][:15]
        train_dataset = dataset[:fold_number * 15] + dataset[fold_number * 15 + 15:]
        accuracy = predict_results(train_dataset, test_dataset, clusters_count)
        accuracies.append(accuracy)
        print(f'Accuracy Fold {fold_number}: f{accuracy:.2f}%')

    print()
    print(f"Average Accuracy: {mean(accuracies):.2f}%")
    print(f"Standard Deviation: {stdev(accuracies):.2f}%")

