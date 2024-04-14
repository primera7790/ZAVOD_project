import warnings

import numpy as np
import pandas
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier

import feature_engineering


def decision_tree(train_data, prod_data, features):
    ''' Обучаем модель и предсказываем целевые значения

    :param train_data: pandas dataframe, содержащий перечень объектов и их принадлежность к конкретному производству
    :param prod_data: pandas dataframe, содержащий перечень объектов среди собранных данных
    :param features: pandas dataframe, являющийся перечнем признаков
    :return: pandas dataframe и 2 .csv файла
    '''
    '''
    train_features - features_train.csv
    train_targets - obj_split_names.csv['manufacture']
    on_prediction_features - features_prod.csv
    unique_objects - obj_unique_from_data.csv
    '''

    train_split_data = feature_engineering.to_objects_split(train_data, train=True)
    train_split_data.index = train_split_data['idx']

    prod_split_data = feature_engineering.to_objects_split(prod_data, prod=True)
    prod_split_data.index = prod_split_data['idx']

    feature_train_data = feature_engineering.feature_engineering(train_split_data, features, train=True)
    feature_train_data.index = feature_train_data['idx']
    del feature_train_data['idx']

    feature_prod_data = feature_engineering.feature_engineering(prod_split_data, features, prod=True)
    feature_prod_data.index = feature_prod_data['idx']
    del feature_prod_data['idx']

    # print(train_split_data)
    # exit()


    X = feature_train_data.iloc[:, 1:]
    y = train_split_data.loc[:, ['manufacture']]

    model = DecisionTreeClassifier()
    model.fit(X, y)

    # test_data = X.loc[X.index == 96]
    to_predict_data = feature_prod_data.iloc[:, 1:]

    # test_prediction = model.predict(test_data)

    # test_prediction = pd.DataFrame(test_prediction)

    # test_prediction.to_csv('data/total_data/test_pred.csv')

    df_proba = pd.DataFrame(model.predict_proba(to_predict_data), columns=model.classes_)
    df_idx = pd.DataFrame(to_predict_data.index)

    dirty_proba = pd.concat([df_idx, df_proba], axis=1)
    total_proba = pd.DataFrame(columns=dirty_proba.columns)
    total_prediction = prod_data
    total_prediction['prediction'] = 'Завод'

    for_analize = pandas.DataFrame(columns=dirty_proba.columns)
    idxs = list()

    for idx in range(dirty_proba['idx'].max() + 1):
        obj_proba = dirty_proba.loc[dirty_proba['idx'] == idx]

        if len(obj_proba.index) > 1:
            sum_proba = np.sum(obj_proba, axis=0).to_numpy()
        else:
            sum_proba = obj_proba.values[0]

        if 'п/ст' in str(prod_data.loc[idx, 'object_name']).lower():
            # print(idx)
            # print(sum_proba)
            sum_proba[2] += 10
            # print(sum_proba)


        # print(unique_objects.loc[idx, 'object_name'])
        # print(sum_proba)
        if len(np.flatnonzero(sum_proba[1:] == np.max(sum_proba[1:]))) > 1:
            # print('yes')
            sum_proba[0] = idx
            for_analize.loc[len(for_analize.index)] = sum_proba
            # print(for_analize)
            # print(unique_objects.loc[idx, 'object_name'])

            idxs.append(prod_data.loc[idx, 'object_name'])

        # if 'п/ст' in str(on_prediction_features.loc[idx, 'object']).lower():
        #     break


        sum_proba[0] = idx
        prediction = df_proba.columns[np.argmax(sum_proba[1:])]

        total_proba.loc[len(total_proba.index)] = sum_proba
        total_prediction.loc[idx, 'prediction'] = prediction

    for_analize['name'] = idxs

    for_analize.to_csv('data/total_data/for_analize.csv')

    total_proba['idx'] = total_proba['idx'].apply(int)


    total_proba.to_csv('data/total_data/total_proba.csv', index=False)
    total_prediction.to_csv('data/total_data/total_prediction.csv')

    # print(dirty_proba)
    # print(train_features.loc[96, 'object'])
    # to_visual_data = pd.DataFrame(index=X.columns, columns=['imp'])
    # to_visual_data['imp'] = model.feature_importances_
    # to_visual_data = to_visual_data.sort_values('imp', ascending=False)

    # plt.bar(to_visual_data.index, to_visual_data['imp'])
    # plt.xticks(rotation=45)
    # plt.show()

    # predictions = model.predict(on_prediction_features)

    return total_prediction


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
        obj_unique_from_data = pd.read_csv('data/total_data/csv/obj_unique_from_data.csv', index_col=0)
        obj_names_data = pd.read_csv('data/total_data/csv/obj_names.csv', index_col=0)
        obj_features = pd.read_csv('data/total_data/csv/obj_features.csv', index_col=0, header=None)

    # dt_predictions = decision_tree(features_train_file, targets_train_file['manufacture'], features_prod_file, obj_unique_from_data)
    dt_predictions = decision_tree(obj_names_data, obj_unique_from_data, obj_features)

    # total_accuracy = accuracy(obj_names['manufacture'], dt_predictions.iloc[:, 1])

    # print(f'Accuracy: {total_accuracy}')


if __name__ == '__main__':
    main()