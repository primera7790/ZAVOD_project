import os
import sys
import warnings
from pathlib import Path

import re
import math
import numpy as np
import pandas as pd
from tqdm.auto import tqdm


''' Блок 1. Необходимые файлы
'''
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    file = pd.read_csv('data/total_data/csv/2_after_knn.csv', index_col=0)
    file2 = pd.read_csv('data/total_data/2_after_knn3.csv', index_col=0)

''' Блок 2. Сравнение между файлами
'''
ff = pd.concat([file[['info', 'requester']], file2[['requester']].rename(columns={'requester': 'req_new'})], axis=1)

ff.loc[ff['requester'] != ff['req_new']].to_csv('data/total_data/unknown.csv')

''' Блок 3. Отображение данных
'''
# uniq_obj_list = file['object'].unique()
# print(len(uniq_obj_list), uniq_obj_list, sep='\n')

''' Блок 4. Визуализация данных
'''