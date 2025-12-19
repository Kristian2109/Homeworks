from ucimlrepo import fetch_ucirepo
from DecisionTree import DecisionTree


def main():
    breast_cancer = fetch_ucirepo(id=14)

    # data (as pandas dataframes)
    x = breast_cancer.data.features
    y = breast_cancer.data.targets

    tree = DecisionTree(5)
    tree.fit(x, y)
    print(tree)


if __name__ == "__main__":
    main()