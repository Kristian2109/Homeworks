import pandas as pd
from statistics import mean, stdev
from sklearn.model_selection import StratifiedKFold
from NaiveBayes import NaiveBayes


def load_dataset():
    initial = pd.read_csv('house-votes-84.data', header=None)
    return initial.rename(columns=dict(zip(initial.columns, get_congregational_voting_headers())))


def get_congregational_voting_headers():
    return list(map(lambda x: x
                    .split('.')[1]
                    .split(':')[0]
                    .strip(), headers.split('\n')))


def get_results_accuracy(model, test):
    results = test.apply(lambda row: model.predict(row) == row['Class Name'], axis=1)
    return mean(results)


def cross_fold_validation(data: pd.DataFrame, ignore_missing: bool):
    skf = StratifiedKFold(
        n_splits=10,
        shuffle=True,
        random_state=42
    )
    y = data['Class Name']

    folds = []
    for train_idx, test_idx in skf.split(data, y):
        x_train = data.iloc[train_idx]
        x_test = data.iloc[test_idx]

        model = NaiveBayes(x_train, 'Class Name', ignore_missing)

        accuracy = get_results_accuracy(model, x_test)
        print(f"    Accuracy Fold {len(folds)}: {accuracy:.2f}%")
        folds.append(accuracy)

    print()
    print(f"    Average Accuracy: {mean(folds):.2f}%")
    print(f"    Standard Deviation: {stdev(folds):2f}%")


headers = """1. Class Name: 2 (democrat, republican)
   2. handicapped-infants: 2 (y,n)
   3. water-project-cost-sharing: 2 (y,n)
   4. adoption-of-the-budget-resolution: 2 (y,n)
   5. physician-fee-freeze: 2 (y,n)
   6. el-salvador-aid: 2 (y,n)
   7. religious-groups-in-schools: 2 (y,n)
   8. anti-satellite-test-ban: 2 (y,n)
   9. aid-to-nicaraguan-contras: 2 (y,n)
  10. mx-missile: 2 (y,n)
  11. immigration: 2 (y,n)
  12. synfuels-corporation-cutback: 2 (y,n)
  13. education-spending: 2 (y,n)
  14. superfund-right-to-sue: 2 (y,n)
  15. crime: 2 (y,n)
  16. duty-free-exports: 2 (y,n)
  17. export-administration-act-south-africa: 2 (y,n)"""
