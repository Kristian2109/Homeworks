from ucimlrepo import fetch_ucirepo
from DecisionTree import DecisionTree
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.metrics import accuracy_score, precision_score, recall_score, make_scorer
from statistics import mean, stdev
import numpy as np


def work(args):
    x_train, y_train, (depth, min_records) = args
    cross_val_sampler = StratifiedKFold(n_splits=10, shuffle=True, random_state=142)
    tree = DecisionTree(depth, min_records)
    scorers = {
        'accuracy': make_scorer(accuracy_score),
        'precision': make_scorer(precision_score, pos_label='recurrence-events'),
        'recall': make_scorer(recall_score, pos_label='recurrence-events')
    }
    scores = cross_validate(tree, x_train, y_train, cv=cross_val_sampler, scoring=scorers)

    scores_formatted = {
        'max_depth': depth,
        'min_records': min_records,
        'average_accuracy': mean(scores['test_accuracy']),
        'accuracy_stddev': stdev(scores['test_accuracy']),
        'average_recall': mean(scores['test_recall']),
        'recall_stddev': stdev(scores['test_recall']),
        'average_precision': mean(scores['test_precision']),
        'precision_stddev': stdev(scores['test_precision'])
    }

    return scores_formatted


def main():
    breast_cancer = fetch_ucirepo(id=14)

    # data (as pandas dataframes)
    x: pd.DataFrame = breast_cancer.data.features
    y: pd.DataFrame = breast_cancer.data.targets

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=105)

    params = []
    for depth in range(2, 6):
        for min_records in [10, 12, 14, 16, 18, 20]:
            params.append((x_train, y_train, (depth, min_records)))

    with ProcessPoolExecutor() as ex:
        results = list(ex.map(work, params))
        best_accuracy = max(results, key=lambda r: r["average_accuracy"])
        best_recall = max(results, key=lambda r: r["average_recall"])
        best_precision = max(results, key=lambda r: r["average_precision"])
        print(best_accuracy)
        print(best_recall)
        print(best_precision)


if __name__ == "__main__":
    main()