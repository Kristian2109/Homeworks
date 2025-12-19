from common import load_dataset, get_results_accuracy, cross_fold_validation, get_percentage
from sklearn.model_selection import train_test_split
from NaiveBayes import NaiveBayes

LAPLACE = 2


def main():
    ignore_missing = bool(input())
    data = load_dataset()
    train, test = train_test_split(data, test_size=0.2, random_state=42)
    model = NaiveBayes(train, 'Class Name', ignore_missing, LAPLACE)
    train_accuracy = get_results_accuracy(model, train)

    print('1. Train Set Accuracy:')
    print(f"    Accuracy: {get_percentage(train_accuracy)}")

    print("10-Fold Cross-Validation Results:")
    cross_fold_validation(train, ignore_missing, 10)

    test_accuracy = get_results_accuracy(model, test)

    print(f"2. Test Set Accuracy:")
    print(f"    Accuracy:{get_percentage(test_accuracy)}")


if __name__ == '__main__':
    main()