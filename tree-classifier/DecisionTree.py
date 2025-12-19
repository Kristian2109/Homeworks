import pandas as pd
import numpy as np
import math


class Node:
    def __init__(self) -> None:
        self.column_name: str | None
        self.children: dict[str, Node] = {}
        self.class_name: str | None


class DecisionTree:
    def __init__(self, max_depth):
        self.max_depth: int = max_depth
        self.tree: None | Node = None

    def fit(self, x: pd.DataFrame, y: pd.DataFrame):
        self.tree = self._build_tree(x, y, 0, self.max_depth)

    def _build_tree(self, x, y, current_depth, max_depth) -> Node:
        current_node = Node()

        if x.columns.size == 0 or current_depth >= max_depth or y.nunique()[y.columns[0]] == 1:
            current_node.class_name = y.mode
            return current_node

        column_entropies = list(map(lambda col: new_entropy(x, y, col), x.columns))
        best_column = x.columns[np.argmin(column_entropies)]
        print(f"Entropies: {column_entropies} - {best_column}")

        current_node.column_name = best_column
        for value, indexes in x.groupby(best_column).groups.items():
            x_partition = x.loc[indexes].drop(columns=[best_column], axis=1)
            y_partition = y.loc[indexes]
            child_node = self._build_tree(x_partition, y_partition, current_depth + 1, max_depth)
            current_node.children.setdefault(value, child_node)

        return current_node


def entropy(y: pd.DataFrame):
    result = 0
    for count in y.value_counts():
        p = count / y.size
        result -= (p * math.log(p))
    return result


def new_entropy(x: pd.DataFrame, y: pd.DataFrame, attribute_name: str):
    counts_by_class = x[attribute_name].value_counts()
    res = 0
    for c in counts_by_class.index:
        partitioned_y = y.loc[x[x[attribute_name] == c].index]
        res += (entropy(partitioned_y) * counts_by_class[c] / y.size)

    return res