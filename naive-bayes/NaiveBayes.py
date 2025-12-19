from pandas import DataFrame, Series
from numpy import argmax
from math import log


class NaiveBayes:
    def __init__(self, train: DataFrame, target_name: str, ignore_missing: bool, laplace_lambda: int = 1):
        self.train = train
        self.target_name = target_name
        self.ignore_missing = ignore_missing
        self.classes = self.train[self.target_name].unique()
        self.laplace_lambda = laplace_lambda

    def predict(self, new_instance: Series):
        classes_counts = self.train[self.target_name].value_counts()
        total_count = self.train.shape[0]
        class_probabilities = (classes_counts + self.laplace_lambda) / total_count + self.classes.size * self.laplace_lambda
        results = []
        for class_index in range(len(class_probabilities)):
            current_class = self.classes[class_index]
            result = log(class_probabilities[current_class])
            for column_name in self.train.columns:
                x = new_instance[column_name]
                if self.ignore_missing and x == '?':
                    continue
                if column_name == self.target_name:
                    continue

                records_for_class = self.train[self.train[self.target_name] == current_class]
                if self.ignore_missing:
                    records_for_class = records_for_class[records_for_class[column_name] != '?']

                class_and_column_count = records_for_class[column_name].value_counts().get(x, 0)
                feature_p_given_class = class_and_column_count + self.laplace_lambda /\
                                        (records_for_class.size + self.classes.size * self.laplace_lambda)

                result += log(feature_p_given_class)

            results.append(result)

        return self.classes[argmax(results)]
