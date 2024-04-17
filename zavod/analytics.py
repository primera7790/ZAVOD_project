import os
import sys
import warnings
from pathlib import Path

import re
import math
import numpy as np
import pandas as pd


''' Блок 1. Необходимые файлы
'''
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    raw_data = pd.read_csv('data_vault/total_data/0_raw_data.csv', index_col=0)
    req = pd.read_csv('data_vault/total_data/csv/requesters.csv')
    chill = pd.read_csv('data_vault/total_data/df_chill_days.csv', index_col=0)
    # file3 = pd.read_csv('data/total_data/csv/1_prepared.csv', index_col=0)
    # file4 = pd.read_csv('data/total_data/csv/obj_split_names.csv', index_col=0)
    # obj_features = pd.read_csv('data/total_data/csv/obj_features.csv', index_col=None, header=None)
    total_data = pd.read_csv('data_vault/total_data/4_total_data.csv', index_col=0)

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
raw_data['date_day'] = pd.to_datetime(raw_data['date_day'])
interval = raw_data['date_day'].max() - raw_data['date_day'].min()


first_day = raw_data['date_day'].min()
last_day = raw_data['date_day'].max()
print(interval.days)

analytics_data = pd.DataFrame(columns=[i for i in range(2017, 2025)] + ['total'])
# analytics_data.loc[0] = 0
print(analytics_data)

''' Блок 4. Визуализация данных
'''

''' Блок 5. Проверка
'''
# print(file4.info())

# f = file.loc[file['requester'] == '', ['object', 'info']]
#
# print(f)

# for i in file['info']:
#     if '' in i:
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



'''
Всего строк: 5062
Рабочих ситуаций: 4046

Всего мастеров: 20
Отмечено уникальных заявителей: 399

Данные с: 2017-07-19
Данные по: 2024-03-01
Всего дней: 2416
Дней с заявками: 1788
Дней без заявок: 628
Соотношение: 2.8 к 1, т.е. из каждых 4х дней на работе приходится 1 чиловый

ПО ГОДАМ разбить на переменные и визуализировать

'''


