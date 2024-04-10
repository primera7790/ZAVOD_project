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


def feature_engineering(data, features, train=False, test=False):
    ''' Превращаем данные в набор признаков

    :param data: pandas dataframe, содержащий подготовленные объекты
    :param features: pandas dataframe, являющийся перечнем желаемых признаков
    :param train: bool, если подготавливаем данные для обучения - True
    :param test: bool, если подготавливаем данные для предсказания - True
    :return: .csv файл
    '''
    ''' 

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
        feature_values_list = [0] * futures_num

        for sym in obj_name:
            sym_dict[sym.lower()] += 1

            alphabet = [chr(i) for i in range(ord('а'), ord('я') + 1)]
            other_symbols = ['.', ',', '/', '-']

            if sym.isdigit() and int(sym) in range(10):
                figures_count += 1

            elif sym.lower() in alphabet:
                letters_count += 1

            else:
                other_symbols_count += 1

            for l_idx in range(len(alphabet)):
                if alphabet[l_idx] in sym_dict:
                    feature_values_list[15 + l_idx] = 1
                    feature_values_list[61 + l_idx] = sym_dict[alphabet[l_idx]]
                else:
                    feature_values_list[15 + l_idx] = 0
                    feature_values_list[61 + l_idx] = 0

            for f in range(10):
                if f in sym_dict:
                    feature_values_list[5 + f] = 1
                    feature_values_list[51 + f] = sym_dict[alphabet[f]]
                else:
                    feature_values_list[5 + f] = 0
                    feature_values_list[51 + f] = 0

            for s_idx in range(len(other_symbols)):
                if other_symbols[s_idx] in sym_dict:
                    feature_values_list[47 + s_idx] = 1
                    feature_values_list[93 + s_idx] = sym_dict[other_symbols[s_idx]]
                else:
                    feature_values_list[47 + s_idx] = 0
                    feature_values_list[93 + s_idx] = 0

            feature_values_list[0] = obj_name
            feature_values_list[1] = symbols_count
            feature_values_list[2] = figures_count
            feature_values_list[3] = letters_count
            feature_values_list[4] = other_symbols_count

        return feature_values_list

    features_data = pd.DataFrame(columns=features.index)

    to_futures = data['object'].apply(lambda x: for_each_object(x, len(features.index)))

    for line in to_futures:
        features_data.loc[len(features_data.index), :] = line

    if train:
        features_data.to_csv('data/total_data/features_train.csv')
    elif test:
        features_data.to_csv('data/total_data/features_test.csv')

    return


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        obj_names_file = pd.read_csv('data/total_data/csv/obj_names.csv', index_col=0)
        obj_split_names_file = pd.read_csv('data/total_data/csv/obj_split_names.csv', index_col=0)
        obj_features = pd.read_csv('data/total_data/csv/obj_features.csv', index_col=0, header=None)

    # to_objects_split(obj_names_file)
    feature_engineering(obj_split_names_file, obj_features, train=True)


if __name__ == '__main__':
    main()