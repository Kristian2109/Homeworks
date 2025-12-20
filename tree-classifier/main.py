from ucimlrepo import fetch_ucirepo
from DecisionTree import DecisionTree
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.metrics import  accuracy_score, precision_score, recall_score, make_scorer


def pr(tree, y_test, r):
    pred = tree.predict_single(r)
    return pred == y_test.loc[r.name]


def main():
    breast_cancer = fetch_ucirepo(id=14)

    # data (as pandas dataframes)
    x: pd.DataFrame = breast_cancer.data.features
    y: pd.DataFrame = breast_cancer.data.targets

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=900)

    tree = DecisionTree(7, 10, 0.01)
    tree.fit(x_train, y_train)
    
    print("res")
    results = x_test.apply(lambda r: pr(tree, y_test, r), axis=1)
    
    print(results['Class'].mean())

    # cross_val_sampler = StratifiedKFold(n_splits=10, shuffle=True, random_state=142)
    # tree = DecisionTree(3, 14, 0.01)
    # scorers = {
    #     'accuracy': make_scorer(accuracy_score),
    #     'precision': make_scorer(precision_score, pos_label='recurrence-events'),
    #     'recall': make_scorer(recall_score, pos_label='recurrence-events')
    # }
    # scores = cross_validate(tree, x_train, y_train, cv=cross_val_sampler, scoring=scorers)
    # print(scores)


if __name__ == "__main__":
    main()