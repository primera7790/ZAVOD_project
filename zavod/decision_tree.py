import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier


def decision_tree(feature_train_data, targets_data, feature_prod_data, obj_names_from_prod):
    ''' Обучаем модель и предсказываем целевые значения

    :param feature_train_data: pandas dataframe, имена тренировочных объектов в признаковом пространстве
    :param targets_data: pandas dataframe, целевые признаки
    :param feature_prod_data: pandas dataframe, имена объектов на предсказание в признаковом пространстве
    :param obj_names_from_prod: pandas dataframe, полные имена объектов на предсказание
    :return: pandas dataframe и 2 .csv файла
    '''

    ''' ОБУЧЕНИЕ МОДЕЛИ
    '''
    X = feature_train_data.iloc[:, 1:]
    y = targets_data.loc[:, ['manufacture']]

    model = DecisionTreeClassifier()
    model.fit(X, y)

    ''' ПРЕДСКАЗАНИЕ ЗНАЧЕНИЙ
    '''
    to_predict_data = feature_prod_data.iloc[:, 1:]

    df_proba = pd.DataFrame(model.predict_proba(to_predict_data), columns=model.classes_)
    df_idx = pd.DataFrame(to_predict_data.index)

    dirty_proba = pd.concat([df_idx, df_proba], axis=1)
    total_proba = pd.DataFrame(columns=dirty_proba.columns)
    total_prediction = obj_names_from_prod
    total_prediction['prediction'] = 'Завод'

    dirty_proba.to_csv('data_vault/total_data/dirty_proba.csv')

    ''' КОРРЕКТИРОВКА ПРЕДСКАЗАНИЙ
    '''

    for idx in range(dirty_proba['idx'].max() + 1):
        obj_proba = dirty_proba.loc[dirty_proba['idx'] == idx]

        if len(obj_proba.index) > 1:
            sum_proba = np.sum(obj_proba, axis=0).to_numpy()
        elif len(obj_proba.index) == 0:
            sum_proba = [0] * 10
            sum_proba[2] = 10
        else:
            sum_proba = obj_proba.values[0]

        if 'п/ст' in str(obj_names_from_prod.loc[idx, 'object_name']).lower():
            sum_proba[2] += 10

        if 'ппп' in str(obj_names_from_prod.loc[idx, 'object_name']).lower():
            sum_proba[3] += 1

        sum_proba[0] = idx
        prediction = df_proba.columns[np.argmax(sum_proba[1:])]

        total_proba.loc[len(total_proba.index)] = sum_proba
        total_prediction.loc[idx, 'prediction'] = prediction

    total_proba['idx'] = total_proba['idx'].apply(int)

    ''' ВИЗУАЛИЗАЦИЯ
    '''

    # to_visual_data = pd.DataFrame(index=X.columns, columns=['imp'])
    # to_visual_data['imp'] = model.feature_importances_
    # to_visual_data = to_visual_data.sort_values('imp', ascending=False)
    #
    # plt.bar(to_visual_data.index, to_visual_data['imp'])
    # plt.xticks(rotation=45)
    # plt.show()


    ''' ЗАВЕРШЕНИЕ
    '''
    # total_proba.to_csv('data/total_data/total_proba.csv', index=False)
    # total_prediction.to_csv('data/total_data/total_prediction.csv')

    return total_prediction


def accuracy(targets, predictions):
    ''' Замер точности предсказаний

    :param targets: pandas series, реальные значения
    :param predictions: pandas series, предсказанные значения
    :return: int, значение точности предсказания [0, 1]
    '''
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

        feature_train_data = pd.read_csv('data_vault/total_data/features_train.csv', index_col=0)
        targets_data = pd.read_csv('data_vault/total_data/obj_split_names.csv', index_col=0)
        feature_prod_data = pd.read_csv('data_vault/total_data/features_prod.csv', index_col=0)
        after_knn = pd.read_csv('data_vault/total_data/2_after_knn.csv', index_col=0)
        obj_names_from_prod = pd.DataFrame({'object_name': after_knn['object']})

        # obj_unique_from_data = pd.read_csv('data/total_data/csv/obj_unique_from_data.csv', index_col=0)

        # obj_from_prod = obj_unique_from_data

    decision_tree(feature_train_data, targets_data, feature_prod_data, obj_names_from_prod)

    # dt_predictions = decision_tree(obj_names_data, obj_from_prod, obj_features)
    # total_accuracy = accuracy(obj_names['manufacture'], dt_predictions.iloc[:, 1])
    # print(f'Accuracy: {total_accuracy}')

    return


if __name__ == '__main__':
    main()