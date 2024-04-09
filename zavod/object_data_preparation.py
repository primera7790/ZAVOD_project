import os
import sys
import warnings
from pathlib import Path

import re
import math
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from collections import defaultdict


def to_objects_split(data):
    ''' Подготовка данных для дальнейшего признакового анализа

    :param data: pandas dataframe, содержащий перечень объектов и их принадлежность к конкретному производству
    :return: .csv file
    '''
    to_correct_list = ['Об.', 'об.', 'Отд.', 'отд.', 'Кор.', 'кор.', 'к.', 'К.']
    new_file = pd.DataFrame(columns=['object', 'manufacture'])
    for obj_idx in range(len(data['object_name'])):
        text = str(data.iloc[obj_idx, 0])

        ''' Пункт 1. Избавляемся от ненужных приписок
        '''
        for cor in to_correct_list:
            if cor in text:
                text = text.replace(cor, '').strip()

        ''' Пункт 2. Сплитуем текст объектов с сохранением привязки к конкретному производству
        '''
        split_list = text.split(' ')
        for el in split_list:
            new_file.loc[len(new_file.index), ['object', 'manufacture']] = [el, data.iloc[obj_idx, 1]]

    new_file.drop_duplicates().to_csv('data/total_data/split_objects.csv')
    # print(split_list)


def feature_engineering(data, features):
    ''' Превращаем данные в набор признаков

    :param data: pandas dataframe, содержащий подготовленные объекты
    :param features: pandas dataframe, являющийся перечнем желаемых признаков
    :return: .csv файл
    '''
    def for_each_object(obj_name, futures_num):
        ''' Проходимся по имени объекта и формируем все признаки

        :param obj_name: obj, отдельно взятое имя объекта
        :param futures_num: int, количество параметров
        :return: list, список, содержащий значения признаков
        '''
        symbols_count = len(obj_name)
        figures_count = 0
        letters_count = 0
        other_symbols_count = 0
        sym_dict = defaultdict(int)

        for sym in obj_name:
            sym_dict[sym] += 1

            alphabet = [chr(i) for i in range(ord('а'), ord('я') + 1)]

            if sym in range(10):
                figures_count += 1

            elif sym in alphabet:
                letters_count += 1

            else:
                other_symbols_count += 1

            feature_values_list = [0] * futures_num

        return []

    features_data = pd.DataFrame(columns=features.index)
    print(len(features.index))

    to_futures = data['object'].apply(lambda x: for_each_object(x, len(features.index)))

    features_data.loc[:] = to_futures

    # for obj in range(len(data['object'])):
        # object_name = data.loc[obj, 'object']

        # values = for_each_object(object_name)

        # feature_values_list = [0] * len(features_data.columns)


        # features_data.loc[len(features_data.index), :] = feature_values_list

        # print(object_name)
        # break
    return



def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        obj_names_file = pd.read_csv('data/total_data/csv/obj_names.csv', index_col=0)
        obj_split_names_file = pd.read_csv('data/total_data/csv/obj_split_names.csv', index_col=0)
        obj_features = pd.read_csv('data/total_data/csv/obj_features.csv', index_col=False, header=None)

    # to_objects_split(obj_names_file)
    feature_engineering(obj_split_names_file, obj_features)


if __name__ == '__main__':
    main()