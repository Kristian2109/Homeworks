import pandas as pd
import numpy as np
import math
from typing import Hashable


class Node:
    def __init__(self) -> None:
        self.column_name: Hashable | None = None
        self.children: dict[Hashable, Node] = {}
        self.class_name: str | None = None


class DecisionTree:
    def __init__(self, max_depth):
        self.max_depth: int = max_depth
        self.tree: None | Node = None

    def fit(self, x: pd.DataFrame, y: pd.DataFrame):
        self.tree = self._build_tree(x, y, 0, self.max_depth)

    def predict(self, value: pd.Series):
        return self._travers_node(self.tree, value)

    def _travers_node(self, node: Node, value: pd.Series):
        if node.class_name:
            return node.class_name

        child = node.children.get(value[node.column_name])
        if not child:
            return None

        return self._travers_node(child, value)

    def _build_tree(self, x: pd.DataFrame, y: pd.DataFrame, current_depth, max_depth) -> Node:
        current_node = Node()

        if x.columns.size == 0 or current_depth >= max_depth or y.nunique()[y.columns[0]] == 1:
            current_node.class_name = y[y.columns[0]].mode().iloc[0]
            return current_node

        column_entropies = list(map(lambda col: partitioned_entropy(x, y, col), x.columns))
        best_column = x.columns[np.argmin(column_entropies)]

        current_node.column_name = best_column
        for value, indexes in x.groupby(best_column).groups.items():
            x_partition = x.loc[indexes].drop(columns=[best_column], axis=1)
            y_partition = y.loc[indexes]
            child_node = self._build_tree(x_partition, y_partition, current_depth + 1, max_depth)
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
