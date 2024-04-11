import warnings

# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier


def decision_tree(train_features, train_targets, on_prediction_features):
    ''' Обучаем модель и предсказываем целевые значения

    :param train_features: pandas dataframe, признаки тренировочных объектов
    :param train_targets: pandas dataframe, содержащий колонку привязки каждого объекта к конкретному производству
    :param on_prediction_features: pandas dataframe, признаки объектов для предсказания целевых значений
    :return: .csv файл
    '''

    X = train_features.iloc[:, 1:]
    y = train_targets['manufacture']

    model = DecisionTreeClassifier()
    model.fit(X, y)

    # test_data = X.loc[X.index == 0]

    test_prediction = model.predict(X)

    test_prediction = pd.DataFrame(test_prediction)

    test_prediction.to_csv('data/total_data/test_pred.csv')


    to_visual_data = pd.DataFrame(index=X.columns, columns=['imp'])
    to_visual_data['imp'] = model.feature_importances_
    to_visual_data = to_visual_data.sort_values('imp', ascending=False)

    plt.bar(to_visual_data.index, to_visual_data['imp'])
    plt.xticks(rotation=45)
    plt.show()



    # predictions = model.predict(on_prediction_features)

    return


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        features_train_file = pd.read_csv('data/total_data/csv/features_train.csv', index_col=0)
        targets_train_file = pd.read_csv('data/total_data/csv/obj_split_names.csv', index_col=0)
        features_test_file = pd.read_csv('data/total_data/csv/features_test.csv', index_col=0)

    decision_tree(features_train_file, targets_train_file, features_test_file)


if __name__ == '__main__':
    main()