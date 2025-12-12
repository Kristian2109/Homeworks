from common import get_iris_dataset, display_statistics, apply_normalization, train_test_split, \
    get_z_normalized, get_min_max_normalized
from knn import predict_results
from random import seed


def test_for_clusters(dataset):
    for k in range(4, 20):
        train, test = train_test_split(dataset, 0.8)
        accuracy = predict_results(train, test, 10)
        print(f"Accuracy {k} clusters: {accuracy:.2f}")


def main():
    seed(100)

    dataset = get_iris_dataset()
    sepal_length = [record[0] for record in dataset]
    sepal_width = [record[1] for record in dataset]
    petal_length = [record[2] for record in dataset]
    petal_width = [record[3] for record in dataset]
    display_statistics("Sepal Length", sepal_length)
    display_statistics("Sepal Width", sepal_width)
    display_statistics("Petal Length", petal_length)
    display_statistics("Petal Width", petal_width)

    print("\n\nNot normalized tests")
    test_for_clusters(dataset)

    z_normalized_dataset = apply_normalization(dataset, get_z_normalized)
    print("\n\nZ normalized tests")
    test_for_clusters(z_normalized_dataset)

    min_max_normalized = apply_normalization(dataset, get_min_max_normalized)
    print("\n\nZ normalized tests")
    test_for_clusters(min_max_normalized)


if __name__ == "__main__":
    main()