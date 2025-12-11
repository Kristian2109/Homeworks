from statistics import mean, stdev, median
from math import ceil
from typing import MutableSequence, Sequence, Tuple
from random import shuffle
from itertools import count
from kdtree import build_tree, Node, search_nearest_neighbors

counter = count()
DIMENSIONALITY = 4
FILE_NAME = "C:\\Users\\krist\\Downloads\\iris\\iris.data"
RECORDS_COUNT_PER_CLASS = 50


def create_record(raw_record: str):
    split = raw_record.split(',')
    return tuple(map(float, split[:-1])) + tuple([split[-1]])


def encode_categorical_values(values: Sequence):
    values_encoding = dict()
    values_set = set()
    current_index = 0

    for v in values:
        if v not in values_set:
            values_encoding[v] = current_index
            values_set.add(v)
            current_index += 1

    return [values_encoding[v] for v in values]


def get_iris_dataset():
    with open(FILE_NAME, "r") as file:
        content = file.read()
        rows = content.split()
        dataset = list(map(create_record, rows))
        target = [r[-1] for r in dataset]
        target_encoded = encode_categorical_values(target)
        return [r[:len(r) - 1] + tuple([target_encoded[index]]) for index, r in enumerate(dataset)]


def display_statistics(name: str, feature_values: list[float]):
    print(f"{name}")
    print(f"Mean: {mean(feature_values):.2f}")
    print(f"Standard deviation: {stdev(feature_values):.2f}")
    print(f"Median: {median(feature_values):.2f}")
    print()


def get_z_normalized(feature_values: list[float]):
    std_dev = stdev(feature_values)
    mean_value = mean(feature_values)

    return list(map(lambda v: (v - mean_value) / std_dev, feature_values))


def get_min_max_normalized(feature_values: list[float]):
    min_value = min(feature_values)
    max_value = max(feature_values)

    return list(map(lambda v: (v - min_value) / (max_value - min_value), feature_values))


def compute_accuracy(results):
    accuracy = sum(map(lambda res: res["best_cluster"] == res["actual_cluster"], results)) / len(results)
    return accuracy


def predict_results(train, test, k):
    tree = build_tree(train)
    results = []
    for r in test:
        result = knn_improved(tree, r, k)
        results.append(result)

    accuracy = compute_accuracy(results)
    return accuracy


def train_test_split(dataset: MutableSequence, train_set_size):
    shuffled_dataset = list(dataset)
    shuffle(shuffled_dataset)

    train = []
    test = []
    train_set_records_per_class = ceil(RECORDS_COUNT_PER_CLASS * train_set_size)
    count_by_class_in_train = {0: 0, 1: 0, 2: 0}

    for i in range(len(shuffled_dataset)):
        current_class = shuffled_dataset[i][-1]
        if count_by_class_in_train.get(current_class) < train_set_records_per_class:
            count_by_class_in_train[current_class] += 1
            train.append(shuffled_dataset[i])
        else:
            test.append(shuffled_dataset[i])

    return train, test


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


def apply_normalization(dataset: Sequence[Sequence], transform_fn):
    features_values = []
    for i in range(4):
        features_values.append([])
        for record in dataset:
            features_values[i].append(record[i])

    normalized_values = [transform_fn(feature) for feature in features_values]
    normalized_dataset = []

    for record_index in range(len(dataset)):
        normalized_dataset.append([])
        for i in range(4):
            normalized_dataset[record_index].append(normalized_values[i][record_index])

        normalized_dataset[record_index].append(dataset[record_index][4])

    return normalized_dataset


def knn_improved(tree: Node, point: Sequence, k: int):
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
