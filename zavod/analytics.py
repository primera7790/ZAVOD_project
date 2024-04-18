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
    raw_prepared_data = pd.read_csv('data_vault/total_data/0_raw_prepared_data.csv', index_col=0)
    chill_data = pd.read_csv('data_vault/total_data/df_chill_days.csv', index_col=0)
    total_data = pd.read_csv('data_vault/total_data/4_total_data.csv', index_col=0)
    requesters_data = pd.read_csv('data_vault/total_data/csv/requesters.csv')

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
raw_prepared_data['date_day'] = pd.to_datetime(raw_prepared_data['date_day'])
total_data['date_day'] = pd.to_datetime(total_data['date_day'])
chill_data['date_day'] = pd.to_datetime(chill_data['date_day'])

analytics_data = pd.DataFrame(columns=[i for i in range(2017, 2025)] + ['total'])


def masters_count(data):
    masters_day = data['master_day']
    masters_night = data['master_night']
    masters = pd.concat([masters_day, masters_night], axis=0) \
        .drop_duplicates().reset_index(drop=True).dropna()
    ans = len(masters)
    return ans


def requesters_count(data):
    requesters = data['requester'].drop_duplicates().reset_index(drop=True)
    ans = len(requesters)
    return ans


def days_count(data):
    days = data['date_day'].drop_duplicates().reset_index(drop=True)
    ans = len(days)
    return ans


def average_time(data):
    actual_data = data.loc[:, ['start_time', 'end_time']].dropna().reset_index(drop=True)

    diffs = list()

    for idx in range(len(actual_data.index)):
        start = pd.to_datetime(
            actual_data['start_time'][idx]
            .replace('[', '').replace(']', '').replace("'", '').replace(',', '')
            .split(' '), format='%H:%M'
        )
        end = pd.to_datetime(
            actual_data['end_time'][idx]
            .replace('[', '').replace(']', '').replace("'", '').replace(',', '')
            .split(' '), format='%H:%M'
        )

        length = len(start) if len(start) <= len(end) else len(end)

        for t in range(length):
            if end[t] > start[t]:
                diff = (end[t] - start[t]).total_seconds() / 60
                diffs.append(diff)

    average = np.average(diffs)
    return average


strings_all = list()
requests_all = list()
days_all = list()
days_work = list()
days_chill = list()
prop_to_one = list()
masters_unique = list()
requesters_unique = list()
requests_per_day = list()
average_max_power = list()
average_min_power = list()
average_24h_power = list()
average_job_time = list()

for v in analytics_data.columns[:-1]:
    r_data = raw_data.loc[raw_data['date_day'].dt.year == v]
    r_p_data = raw_prepared_data.loc[raw_prepared_data['date_day'].dt.year == v]
    t_data = total_data.loc[total_data['date_day'].dt.year == v]
    c_data = chill_data.loc[chill_data['date_day'].dt.year == v]

    str_v = len(r_data.index)
    req_v = len(t_data.index)
    day_a_v = days_count(r_data)
    day_w_v = days_count(t_data)
    day_c_v = days_count(c_data)
    prop_v = round(day_w_v / day_c_v, 2)
    mast_v = masters_count(t_data)
    rqvstrs_v = requesters_count(t_data)
    rqvstrs_p_d_v = round(req_v / day_w_v, 2)
    max_v = round(np.average(r_p_data['max_power'].dropna()), 2)
    min_v = round(np.average(r_p_data['min_power'].dropna()), 2)
    pow24_v = round(np.average(r_p_data['power_per_24_hours'].dropna()), 2)
    av_time_v = average_time(t_data)


    strings_all.append(str_v)
    requests_all.append(req_v)
    days_all.append(day_a_v)
    days_work.append(day_w_v)
    days_chill.append(day_c_v)
    prop_to_one.append(prop_v)
    masters_unique.append(mast_v)
    requesters_unique.append(rqvstrs_v)
    requests_per_day.append(rqvstrs_p_d_v)
    average_max_power.append(max_v)
    average_min_power.append(min_v)
    average_24h_power.append(pow24_v)
    average_job_time.append(av_time_v)

strings_all.append(len(raw_data.index))
requests_all.append(len(total_data.index))
days_all.append(days_count(raw_data))
days_work.append(days_count(total_data))
days_chill.append(days_count(chill_data))
prop_to_one.append(round(days_count(total_data) / days_count(chill_data), 2))
masters_unique.append(masters_count(total_data))
requesters_unique.append(requesters_count(total_data))
requests_per_day.append(round(len(total_data.index) / days_count(total_data), 2))
average_max_power.append(round(np.average(raw_prepared_data['max_power'].dropna()), 2))
average_min_power.append(round(np.average(raw_prepared_data['min_power'].dropna()), 2))
average_24h_power.append(round(np.average(raw_prepared_data['power_per_24_hours'].dropna()), 2))
average_job_time.append(average_time(total_data))

analytics_data.loc['strings_all'] = strings_all
analytics_data.loc['requests_all'] = requests_all
analytics_data.loc['days_all'] = days_all
analytics_data.loc['days_work'] = days_work
analytics_data.loc['days_chill'] = days_chill
analytics_data.loc['prop_to_one'] = prop_to_one
analytics_data.loc['masters_unique'] = masters_unique
analytics_data.loc['requesters_unique'] = requesters_unique
analytics_data.loc['requests_per_day'] = requests_per_day
analytics_data.loc['average_max_power'] = average_max_power
analytics_data.loc['average_min_power'] = average_min_power
analytics_data.loc['average_24h_power'] = average_24h_power
analytics_data.loc['average_job_time'] = average_job_time

print(analytics_data)


''' Блок 4. Визуализация данных
'''

''' Блок 5. Проверка
'''

''' Архивный блок. 
'''





'''
Всего строк: 5062
Рабочих ситуаций: 4046

Всего мастеров: 20
Отмечено уникальных заявителей: 399

Данные с: 2017-07-19
Данные по: 2024-03-01
Всего рассмотрено дней: 2416?
Дней с заявками: 1788
Дней без заявок: 628
Соотношение: 2.8 к 1, т.е. из каждых 4х дней на работе приходится 1 чиловый

ПО ГОДАМ разбить на переменные и визуализировать

'''


