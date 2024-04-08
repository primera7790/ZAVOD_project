import os
import sys
import warnings
from pathlib import Path

import re
import math
import numpy as np
import pandas as pd
from tqdm.auto import tqdm


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


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        file = pd.read_csv('data/total_data/csv/obj_names.csv', index_col=0)

    to_objects_split(file)


if __name__ == '__main__':
    main()