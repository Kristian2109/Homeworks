import pandas as pd
import numpy as np
import math
import sklearn as sk
from typing import Hashable


class Node:
    def __init__(self, majority_class) -> None:
        self.column_name: Hashable | None = None
        self.children: dict[Hashable, Node] = {}
        self.class_name: str | None = None
        self.majority_class: str = majority_class


class DecisionTree(sk.base.BaseEstimator):
    def __init__(self, max_depth=100, min_examples=0, min_entropy_gain=0.005):
        self.max_depth: int = max_depth
        self.min_examples: int = min_examples
        self.min_entropy_gain: float = min_entropy_gain
        self.tree: None | Node = None

    def fit(self, x: pd.DataFrame, y: pd.DataFrame):
        self.tree = self._build_tree(x, y, 0)

    def predict(self, x: pd.DataFrame) -> np.ndarray:
        return x.apply(self.predict_single, axis=1).to_numpy()

    def predict_single(self, value: pd.Series) -> str | None:
        return self._travers_node(self.tree, value)

    def _travers_node(self, node: Node, value: pd.Series):
        if node.class_name:
            return node.class_name

        child = node.children.get(value[node.column_name])
        if not child:
            return node.majority_class

        return self._travers_node(child, value)

    def _build_tree(self, x: pd.DataFrame, y: pd.DataFrame, current_depth) -> Node:
        majority_class = y[y.columns[0]].mode().iloc[0]
        current_node = Node(majority_class)

        if x.columns.size == 0 or \
                current_depth >= self.max_depth or \
                y.nunique()[y.columns[0]] == 1 or \
                y.size < self.min_examples:
            current_node.class_name = majority_class
            return current_node

        column_entropies = list(map(lambda col: partitioned_entropy(x, y, col), x.columns))
        best_column = x.columns[np.argmin(column_entropies)]

        if entropy(y) - min(column_entropies) < self.min_entropy_gain:
            current_node.class_name = majority_class
            return current_node

        current_node.column_name = best_column
        for value, indexes in x.groupby(best_column).groups.items():
            x_partition = x.loc[indexes].drop(columns=[best_column], axis=1)
            y_partition = y.loc[indexes]
            child_node = self._build_tree(x_partition, y_partition, current_depth + 1)
            current_node.children.setdefault(value, child_node)

        return current_node


def partitioned_entropy(x: pd.DataFrame, y: pd.DataFrame, column_name: str):
    counts_by_class = x[column_name].value_counts()
    res = 0
    for c in counts_by_class.index:
        partitioned_y = y.loc[x[x[column_name] == c].index]
        res += (entropy(partitioned_y) * counts_by_class[c] / y.size)

    return res


def entropy(y: pd.DataFrame):
    result = 0
    for count in y.value_counts():
        p = count / y.size
        result -= (p * math.log(p))
    return result
