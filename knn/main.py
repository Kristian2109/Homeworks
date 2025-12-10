import math
from statistics import mean, stdev, median
from math import sqrt
from typing import Sequence
from random import shuffle, seed
FILE_NAME = "C:\\Users\\krist\\Downloads\\iris\\iris.data"


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


def get_dataset():
    with open(FILE_NAME, "r") as file:
        content = file.read()
        rows = content.split()
        dataset = list(map(create_record, rows))
        target = [r[-1] for r in dataset]
        print(target)
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
    # print(distances)

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


def main():
    dataset = get_dataset()
    sepal_length = [record[0] for record in dataset]
    sepal_width = [record[1] for record in dataset]
    petal_length = [record[2] for record in dataset]
    petal_width = [record[3] for record in dataset]
    display_statistics("Sepal Length", sepal_length)
    display_statistics("Sepal Width", sepal_width)
    display_statistics("Petal Length", petal_length)
    display_statistics("Petal Width", petal_width)

    # Conclusion: Requires Normalization
    # print(get_z_normalized(petal_width))
    print(dataset)

    seed(67601)
    records_count = len(dataset)
    train_count = math.ceil(records_count * 0.8)
    test_count = records_count - train_count

    shuffle(dataset)
    train = dataset[:train_count]
    test = dataset[test_count:]
    for k in range(1, 20):
        accuracy = predict_results(train, test, k)
        print(f"{k} - Accuracy {accuracy:.2f}")

    accuracies: list[float] = []
    for fold_number in range(10):
        test_dataset = dataset[fold_number * 15:][:15]
        train_dataset = dataset[:fold_number * 15] + dataset[fold_number * 15 + 15:]
        accuracy = predict_results(train_dataset, test_dataset, 10)
        accuracies.append(accuracy)
        print(f'Accuracy Fold {fold_number}: f{accuracy:.2f}%')

    print(f"Average Accuracy: {mean(accuracies):.2f}%")
    print(f"Standard Deviation: {stdev(accuracies):.2f}%")


if __name__ == "__main__":
    main()