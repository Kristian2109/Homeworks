from knn import get_iris_dataset, display_statistics, get_z_normalized, predict_results, train_test_split


def main():
    dataset = get_iris_dataset()
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

    normalized_dataset = []
    features_values = []
    for i in range(4):
        features_values.append([])
        for record in dataset:
            features_values[i].append(record[i])

    normalized_values = [get_z_normalized(feature) for feature in features_values]

    for record_index in range(len(dataset)):
        for i in range(4):
            normalized_dataset.append(normalized_values[i][record_index])

        normalized_values.append(dataset[record_index][4])

    for k in range(4, 20):
        train, test = train_test_split(dataset, 0.8)
        accuracy = predict_results(train, test, 10)
        print(f"Accuracy {k} clusters: {accuracy:.2f}")


if __name__ == "__main__":
    main()