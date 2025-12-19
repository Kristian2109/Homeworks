from ucimlrepo import fetch_ucirepo
from DecisionTree import DecisionTree
from sklearn.model_selection import train_test_split
from statistics import mean


def pr(tree, y_test, r):
    pred = tree.predict(r)
    print(f"Pred {pred}; Actual {y_test.loc[r.name]}")
    return pred == y_test.loc[r.name]


def main():
    breast_cancer = fetch_ucirepo(id=14)

    # data (as pandas dataframes)
    x = breast_cancer.data.features
    y = breast_cancer.data.targets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=105)

    tree = DecisionTree(3)
    tree.fit(x_train, y_train)

    print("res")
    results = x_test.apply(lambda r: pr(tree, y_test, r), axis=1)

    print(results['Class'].mean())


if __name__ == "__main__":
    main()