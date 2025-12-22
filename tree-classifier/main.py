from ucimlrepo import fetch_ucirepo
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold

from DecisionTree import DecisionTree

BASE_MAX_DEPTH = 4
BASE_MIN_EXAMPLES = 14
BASE_MIN_GAIN = 0.02


def pct(x): 
    return f"{x * 100:.2f}%"


def acc(model, X, y):
    y_true = y.iloc[:, 0].to_numpy()
    y_pred = model.predict(X)
    return float(np.mean(y_pred == y_true))


def parse_mode():
    parts = input().strip().split()
    return int(parts[0])



def train_and_eval(X_train, y_train, X_test, y_test, **params):
    model = DecisionTree(**params)
    model.fit(X_train, y_train)

    train_acc = acc(model, X_train, y_train)
    test_acc = acc(model, X_test, y_test)

    print("1. Train Set Accuracy:")
    print(f"    Accuracy: {pct(train_acc)}\n")

    # 10-fold CV
    print("10-Fold Cross-Validation Results:\n")
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    fold_scores = []

    y_strat = y_train.iloc[:, 0]
    for i, (tr_idx, val_idx) in enumerate(skf.split(X_train, y_strat), start=1):
        X_tr, y_tr = X_train.iloc[tr_idx], y_train.iloc[tr_idx]
        X_val, y_val = X_train.iloc[val_idx], y_train.iloc[val_idx]


        m = DecisionTree(**params)
        m.fit(X_tr, y_tr)

        a = acc(m, X_val, y_val)
        fold_scores.append(a)
        print(f"    Accuracy Fold {i}: {pct(a)}")

    fold_scores = np.array(fold_scores)
    print(f"\n    Average Accuracy: {pct(fold_scores.mean())}")
    print(f"    Standard Deviation: {pct(fold_scores.std())}\n")

    print("2. Test Set Accuracy:")
    print(f"    Accuracy: {pct(test_acc)}")


def main():
    mode = parse_mode()

    breast_cancer = fetch_ucirepo(id=14)
    X: pd.DataFrame = breast_cancer.data.features
    y: pd.DataFrame = breast_cancer.data.targets

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y.iloc[:, 0]
    )

    max_depth = 100 if mode == 1 else BASE_MAX_DEPTH
    min_examples = 1 if mode == 0 else BASE_MIN_EXAMPLES

    train_and_eval(X_train, y_train, X_test, y_test, max_depth=max_depth, min_examples=min_examples, min_entropy_gain=BASE_MIN_GAIN)


if __name__ == "__main__":
    main()
