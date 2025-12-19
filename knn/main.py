from statistics import mean, stdev
from knn import predict_results
from common import train_test_split, get_iris_dataset
from random import seed, shuffle


TRAIN_SET_SIZE: float = 0.8


def main():
    clusters_count = int(input())
    dataset = get_iris_dataset()

    seed(1799)
    train, test = train_test_split(dataset, TRAIN_SET_SIZE)

    accuracy = predict_results(train, train, clusters_count)
    print("Train set accuracy")
    print(f"{clusters_count} - Accuracy: {accuracy:.2f}")
    print()

    accuracies: list[float] = []
    shuffle(dataset)
    for fold_number in range(10):
        test_dataset = dataset[fold_number * 15:][:15]
        train_dataset = dataset[:fold_number * 15] + dataset[fold_number * 15 + 15:]
        accuracy = predict_results(train_dataset, test_dataset, clusters_count)
        accuracies.append(accuracy)
        print(f'Accuracy Fold {fold_number}: {accuracy:.2f}%')

    print()
    print(f"Average Accuracy: {mean(accuracies):.2f}%")
    print(f"Standard Deviation: {stdev(accuracies):.2f}%")

    accuracy = predict_results(train, test, clusters_count)

    print("\n\nTrain set accuracy")
    print(f"{clusters_count} - Accuracy: {accuracy:.2f}")
    print()


if __name__ == "__main__":
    main()