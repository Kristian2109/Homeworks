from knn import get_iris_dataset, display_statistics


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


if __name__ == "__main__":
    main()