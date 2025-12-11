from statistics import mean, stdev, median
from math import sqrt, ceil
from typing import MutableSequence, Sequence
from random import shuffle


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


def min_max_normalized(feature_values: list[float]):
    min_value = min(feature_values)
    max_value = max(feature_values)

    return list(map(lambda v: (v - min_value) / (max_value - min_value), feature_values))


def euclidean_distance(first: Sequence, second: Sequence):
    seq_len = len(first)
    non_squared_distance: float = 0.
    for i in range(seq_len):
        non_squared_distance += (first[i] - second[i]) ** 2

    return sqrt(non_squared_distance)


def knn(records: list[Sequence], point: Sequence, k: int):
    distances = list(map(lambda r: (euclidean_distance(r[:-1], point[:-1]), r[-1]), records))
    sorted_distances = sorted(distances, key=lambda distance: distance[0])
    best_k = sorted_distances[:k]
    values_count = [0] * 10

    for v in best_k:
        values_count[v[1]] += 1

    best = -10000000
    best_index = -100000
    for index, count in enumerate(values_count):
        if best < count:
            best_index = index
            best = count

    return {
        "best_cluster": best_index,
        "actual_cluster": point[-1]
    }


def compute_accuracy(results):
    accuracy = sum(map(lambda res: res["best_cluster"] == res["actual_cluster"], results)) / len(results)
    return accuracy


def predict_results(train, test, k):
    results = []
    for r in test:
        result = knn(train, r, k)
        results.append(result)

    accuracy = compute_accuracy(results)
    return accuracy


def train_test_split(dataset: MutableSequence, train_set_size):
    shuffled_dataset = list(dataset)
    shuffle(shuffled_dataset)

    records_count = len(shuffled_dataset)

    train = []
    test = []
    classes_in_train = {0: 0, 1: 0, 2: 0}
    train_set_records_per_class = ceil(RECORDS_COUNT_PER_CLASS * train_set_size)

    for i in range(records_count):
        current_class = shuffled_dataset[i][-1]
        if classes_in_train.get(current_class) < train_set_records_per_class:
            classes_in_train[current_class] += 1
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
