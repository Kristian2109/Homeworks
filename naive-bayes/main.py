from common import load_dataset, get_results_accuracy, cross_fold_validation
from sklearn.model_selection import train_test_split
from NaiveBayes import NaiveBayes


def main():
    ignore_missing = bool(input())
    data = load_dataset()
    train, test = train_test_split(data, test_size=0.2)
    model = NaiveBayes(train, 'Class Name', ignore_missing)
    # train_accuracy = get_results_accuracy(model, train)

    # print('1. Train Set Accuracy:')
    # print(f"    Accuracy: {train_accuracy:.2f}%")

    print("10-Fold Cross-Validation Results:")
    cross_fold_validation(train, ignore_missing)


if __name__ == '__main__':
    main()