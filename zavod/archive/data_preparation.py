import os
import warnings

import pandas as pd
from dotenv import load_dotenv


def after_data_mining():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        file = pd.read_csv('data/total_data/csv/0_total_table.csv', index_col=0)

    file.loc[file['max_power'] == file['max_power'].max(), ['max_power', 'min_power', 'power_per_24_hours']] = 77, 80, 1914

    while file['power_per_24_hours'].max() > 3000:
        max_24 = file['power_per_24_hours'].max()
        file.loc[file['power_per_24_hours'] == max_24, 'power_per_24_hours'] = int(str(int(max_24))[:-1])

    file.loc[file['max_power'] == file['max_power'].max(), ['max_power', 'min_power']] = pd.NA

    file['date_day'] = pd.to_datetime(file['date_day']).dt.normalize()
    file['date_night'] = pd.to_datetime(file['date_night']).dt.normalize()
    file.loc[file['date_day'] == file['date_night'], 'date_night'] += pd.Timedelta('1 day')

    null_criterion_list = ['отказов в работе электрооборудования и электроснабжения не было', 'отказа электрооборудования, сетей электроснабжения нет',
                           'отказа электрооборудования, сетей электроснабжения не было', 'неисправности, отказа электрооборудования, сетей электроснабжения не было',
                           'неисправности, отказа электрооборудования, сетей электроснабжения нет.', 'неисправности, отказа электрооборудования, сетей электроснабжения нет',
                           'Неисправностей, отказа электрооборудования, сетей электроснабжения не было', 'отказа электрооборудования, сетей электроснабжения небыло.',
                           'отказа электрооборудования, сетей электроснабжения- нет', 'Неисправности ,отказа электрооборудования не было.']

    null_idx_list = list(file.loc[file['info'].isnull()].index)
    for criterion in null_criterion_list:
        idx_list = list(file.loc[file['info'] == criterion].index)
        null_idx_list.extend(idx_list)

    df_chill_days = file.loc[null_idx_list, :]

    df_work_days = file.drop(index=df_chill_days.index).reset_index(drop=True)
    df_work_days.loc[df_work_days['start_time'].notna()].apply(lambda x: str(x).split())
    df_work_days.loc[df_work_days['end_time'].notna()].apply(lambda x: str(x).split())

    df_work_days.to_csv('data/total_data/1_preparationed.csv')
    return


def after_knn():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        file = pd.read_csv('data/total_data/csv/2_after_knn.csv', index_col=0)

    load_dotenv('data/env/.env')
    surname_list = os.environ.get('surname_list').split('_')

    for sur_idx in range(len(surname_list)):
        sur = surname_list[sur_idx].split(' ')[0]
        file_sur_filter = file.loc[file['requester'] == surname_list[sur_idx]]
        info_filter = file_sur_filter['info']

        true_sur_list = list()
        info_filter.apply(lambda x: true_sur_list.append(sur) if sur in x else true_sur_list.append('не указан'))

        file.loc[file_sur_filter.index, 'requester'] = true_sur_list

        file.to_csv('data/total_data/prep2.csv')


def main(after_data_mining=None, after_knn=None):
    if after_data_mining:
        after_data_mining()
    elif after_knn:
        after_knn()
    return


if __name__ == '__main__':
    main(after_knn)