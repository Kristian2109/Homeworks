from pandas import DataFrame, Series
from numpy import argmax
from math import log


class NaiveBayes:
    def __init__(self, train: DataFrame, target_name: str, ignore_missing: bool):
        self.train = train
        self.target_name = target_name
        self.ignore_missing = ignore_missing

    def predict(self, new_instance: Series):
        classes = self.train[self.target_name].unique()
        classes_counts = self.train[self.target_name].value_counts()
        total_count = self.train.shape[0]
        class_probabilities = classes_counts / total_count
        results = []
        for class_index in range(len(class_probabilities)):
            current_class = classes[class_index]
            result = log(class_probabilities[current_class])
            for column_name in self.train.columns:
                if self.ignore_missing and new_instance[column_name] == '?':
                    continue
                if column_name == self.target_name:
                    continue

                records_for_class = self.train[self.train[self.target_name] == current_class]
                if self.ignore_missing:
                    records_for_class = records_for_class[records_for_class[column_name] != '?']

                feature_p_given_class = records_for_class[column_name].value_counts()[new_instance[column_name]] / \
                                        records_for_class.size

                result += log(feature_p_given_class)

            results.append(result)

        return classes[argmax(results)]
