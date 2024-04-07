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
    file2 = pd.read_csv('data/total_data/csv/requesters.csv', index_col=0)
    file3 = pd.read_csv('data/total_data/csv/1_prepared.csv', index_col=0)
    # file4 = pd.read_csv('data/total_data/1_prepared.csv', index_col=0)

''' Блок 2. Сравнение между файлами
'''
# ff = pd.concat([file[['info', 'requester']], file2[['requester']].rename(columns={'requester': 'req_new'})], axis=1)
#
# ff.loc[ff['requester'] != ff['req_new']].to_csv('data/total_data/unknown.csv')

# print(file3.info())
# print(file4.info())
# print(file3.describe())
# print(file4.describe())

''' Блок 3. Агрегация данных
'''


''' Блок 4. Визуализация данных
'''

''' Блок 5. Проверка
'''
f = file.loc[file['requester'] == '', ['object', 'info']]

print(f)

# for i in file['info']:
#     if 'Шакир' in i:
#         print(i)

''' Архивный блок. 
'''
# Поиск опечаток и схожих фамилий
# llist = list()
# for i in tqdm(file2.loc[:, 'requester_name']):
#     for j in file2.loc[:, 'requester_name']:
#         llist.appendsplit(' ')[0] == j.split(' ')[0] and i != j else None
# # ff = pd.DataFrame(columns=['name'])
# # for k in tqdm(llist):
# #     ff.loc[len(ff.index), 'name'] = k[0]
# #     ff.loc[len(ff.index), 'name'] = k[1]
# #
# # ff = ff.sort_values('name')
# # ff = pd.DataFrame(ff['name'].unique())
#
# # f = pd.DataFrame()
# # for i in tqdm(ff['name']):
# #     f = pd.concat([f, file.loc[file['requester'] == i, ['requester', 'max_power']].groupby('requester').count().reset_index()])
# #
# # print(f)
# # ff.to_csv('data/total_data/1_0.csv')
#
# # pd.DataFrame({'name': ff}).to_cs('d([i, j]) if i.ata/total_data/without_0.csv')






