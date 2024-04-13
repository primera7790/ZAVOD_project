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

    # test_data = X.loc[X.index == 96]
    test_data = X

    test_prediction = model.predict(test_data)

    test_prediction = pd.DataFrame(test_prediction)

    # test_prediction.to_csv('data/total_data/test_pred.csv')

    df_proba = pd.DataFrame(model.predict_proba(test_data), columns=model.classes_)
    df_idx = pd.DataFrame(train_features.index)

    total_proba = pd.concat([df_idx, df_proba], axis=1)
    total_proba.to_csv('data/total_data/total_proba.csv')
    # print(total_proba)
    # print(train_features.loc[96, 'object'])
    # to_visual_data = pd.DataFrame(index=X.columns, columns=['imp'])
    # to_visual_data['imp'] = model.feature_importances_
    # to_visual_data = to_visual_data.sort_values('imp', ascending=False)

    # plt.bar(to_visual_data.index, to_visual_data['imp'])
    # plt.xticks(rotation=45)
    # plt.show()

    # predictions = model.predict(on_prediction_features)

    return test_prediction


def accuracy(targets, predictions):
    obj_num = len(targets)
    loss_count = 0

    for idx in range(obj_num):
        loss_count += 1 if targets[idx] != predictions[idx] else 0

    print(loss_count, obj_num, sep='\n')
    total_accuracy = 1 - loss_count / obj_num

    return total_accuracy


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        features_train_file = pd.read_csv('data/total_data/csv/features_train.csv', index_col=0)
        targets_train_file = pd.read_csv('data/total_data/csv/obj_split_names.csv', index_col=0)
        features_prod_file = pd.read_csv('data/total_data/csv/features_prod.csv', index_col=0)

    dt_predictions = decision_tree(features_train_file, targets_train_file, features_prod_file)

    targets_train_file = targets_train_file.reset_index(drop=True)
    dt_predictions = dt_predictions.reset_index(drop=True)

    # total_accuracy = accuracy(targets_train_file['manufacture'], dt_predictions.iloc[:, 0])
    print(dt_predictions.iloc[0, 0])
    # print(f'Accuracy: {total_accuracy}')


if __name__ == '__main__':
    main()