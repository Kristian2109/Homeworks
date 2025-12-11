import math
from statistics import mean, stdev, median
from knn import get_iris_dataset, predict_results
from random import shuffle, seed


TRAIN_SET_SIZE: int = 0.8

def main():
    clusters_count = int(input())
    dataset = get_iris_dataset()

    seed(671010)
    records_count = len(dataset)
    train_count = math.ceil(records_count * TRAIN_SET_SIZE)

    shuffle(dataset)
    train = dataset[:train_count]

    accuracy = predict_results(train, train, clusters_count)
    print("Train set accuracy")
    print(f"{clusters_count} - Accuracy: {accuracy:.2f}")
    print()

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


if __name__ == "__main__":
    main()