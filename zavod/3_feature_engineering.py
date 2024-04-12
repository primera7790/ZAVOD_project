import warnings

import pandas as pd
from collections import defaultdict


def to_objects_split(data, train=False, prod=False):
    ''' Подготовка данных для дальнейшего признакового анализа

    :param data: pandas dataframe, содержащий перечень объектов и их принадлежность к конкретному производству
    :param train: bool, если подготавливаем данные для обучения - True
    :param prod: bool, если подготавливаем данные для предсказания - True
    :return: .csv file
    '''
    to_correct_list = ['Об.', 'об.', 'Отд.', 'отд.', 'Кор.', 'кор.', 'к.', 'К.', 'Отд']

    if train:
        new_file = pd.DataFrame(columns=['idx', 'object', 'manufacture'])
    elif prod:
        new_file = pd.DataFrame(columns=['idx', 'object'])

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
        split_list = [s for s in split_list if s and s not in ('nan', '', '\n', 'и')]

        for el in split_list:

            if train:
                new_file.loc[len(new_file.index), ['idx', 'object', 'manufacture']] = [obj_idx, el, data.iloc[obj_idx, 1]]
            elif prod:
                new_file.loc[len(new_file.index), ['idx', 'object']] = [obj_idx, el]

    if train:
        new_file.drop_duplicates().to_csv('data/total_data/obj_split_names.csv', index=False)
    elif prod:
        new_file.drop_duplicates().to_csv('data/total_data/obj_split_names_from_data.csv', index=False)


def feature_engineering(data, features, train=False, prod=False):
    ''' Превращаем данные в набор признаков

    :param data: pandas dataframe, содержащий подготовленные объекты
    :param features: pandas dataframe, являющийся перечнем желаемых признаков
    :param train: bool, если подготавливаем данные для обучения - True
    :param prod: bool, если подготавливаем данные для предсказания - True
    :return: .csv файл
    '''
    ''' 

    :param data: pandas dataframe, содержащий подготовленные объекты
    :param features: pandas dataframe, являющийся перечнем желаемых признаков
    :return: .csv файл
    '''

    def for_each_object(obj_name, features_num):
        ''' Проходимся по имени объекта и формируем все признаки

        :param obj_name: obj, отдельно взятое имя объекта
        :param features_num: int, количество параметров
        :return: list, список, содержащий значения признаков
        '''
        obj_name = str(obj_name)
        symbols_count = len(obj_name)
        figures_count = 0
        letters_count = 0
        other_symbols_count = 0
        figure_first = 0
        sym_dict = defaultdict(int)
        feature_values_list = [0] * features_num

        for sym in obj_name:
            sym_dict[sym.lower()] += 1

            alphabet = [chr(i) for i in range(ord('а'), ord('я') + 1)]
            other_symbols = ['.', ',', '/', '-']

            if sym.isdigit() and int(sym) in range(10):
                figures_count += 1
                figure_first = int(sym) if figures_count == 1 else figure_first

            elif sym.lower() in alphabet:
                letters_count += 1

            else:
                other_symbols_count += 1

            for l_idx in range(len(alphabet)):
                if alphabet[l_idx] in sym_dict:
                    feature_values_list[17 + l_idx] = 1
                    feature_values_list[63 + l_idx] = sym_dict[alphabet[l_idx]]
                else:
                    feature_values_list[17 + l_idx] = 0
                    feature_values_list[63 + l_idx] = 0

            for f in range(10):
                if str(f) in sym_dict:
                    feature_values_list[7 + f] = 1
                    feature_values_list[53 + f] = sym_dict[str(f)]
                else:
                    feature_values_list[7 + f] = 0
                    feature_values_list[53 + f] = 0

            for s_idx in range(len(other_symbols)):
                if other_symbols[s_idx] in sym_dict:
                    feature_values_list[49 + s_idx] = 1
                    feature_values_list[95 + s_idx] = sym_dict[other_symbols[s_idx]]
                else:
                    feature_values_list[49 + s_idx] = 0
                    feature_values_list[95 + s_idx] = 0

            feature_values_list[1] = obj_name
            feature_values_list[2] = symbols_count
            feature_values_list[3] = figures_count
            feature_values_list[4] = letters_count
            feature_values_list[5] = other_symbols_count
            feature_values_list[6] = figure_first

        return feature_values_list

    features_data = pd.DataFrame(columns=features.index)


    to_futures = data['object'].apply(lambda x: for_each_object(x, len(features.index)))

    for line in to_futures:
        features_data.loc[len(features_data.index), :] = line

    features_data['idx'] = data.index

    if train:
        features_data.to_csv('data/total_data/features_train.csv', index=False)
    elif prod:
        features_data.to_csv('data/total_data/features_prod.csv', index=False)

    return


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        obj_names_file = pd.read_csv('data/total_data/csv/obj_names.csv', index_col=0)
        obj_unique_from_data_file = pd.read_csv('data/total_data/csv/obj_unique_from_data.csv', index_col=0)

        obj_split_names_file = pd.read_csv('data/total_data/csv/obj_split_names.csv', index_col=0)
        obj_split_names_from_data_file = pd.read_csv('data/total_data/csv/obj_split_names_from_data.csv', index_col=0)

        obj_features = pd.read_csv('data/total_data/csv/obj_features.csv', index_col=0, header=None)

    # to_objects_split(obj_names_file, train=True)
    feature_engineering(obj_split_names_file, obj_features, train=True)


if __name__ == '__main__':
    main()