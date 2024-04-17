import warnings

import pandas as pd


def main_preparation(data):
    ''' Корректировка и стандартизация данных, переданных сразу после сбора

    :param data: pandas dataframe, содержащий собранные данные без обработки
    :return: pandas dataframe
    '''

    data.loc[data['max_power'] == data['max_power'].max(), ['max_power', 'min_power', 'power_per_24_hours']] = 77, 80, 1914

    while data['power_per_24_hours'].max() > 3000:
        max_24 = data['power_per_24_hours'].max()
        data.loc[data['power_per_24_hours'] == max_24, 'power_per_24_hours'] = int(str(int(max_24))[:-1])

    data.loc[data['max_power'] == data['max_power'].max(), ['max_power', 'min_power']] = pd.NA

    data['date_day'] = pd.to_datetime(data['date_day']).dt.normalize()
    data['date_night'] = pd.to_datetime(data['date_night']).dt.normalize()
    data.loc[data['date_day'] == data['date_night'], 'date_night'] += pd.Timedelta('1 day')

    null_criterion_list = ['отказов в работе электрооборудования и электроснабжения не было', 'отказа электрооборудования, сетей электроснабжения нет',
                           'отказа электрооборудования, сетей электроснабжения не было', 'неисправности, отказа электрооборудования, сетей электроснабжения не было',
                           'неисправности, отказа электрооборудования, сетей электроснабжения нет.', 'неисправности, отказа электрооборудования, сетей электроснабжения нет',
                           'Неисправностей, отказа электрооборудования, сетей электроснабжения не было', 'отказа электрооборудования, сетей электроснабжения небыло.',
                           'отказа электрооборудования, сетей электроснабжения- нет', 'Неисправности ,отказа электрооборудования не было.']

    for col in data.columns[2:]:
        data[col] = data[col].apply(lambda x: pd.NA if str(x).strip() == '' else x)

    null_idx_list = list(data.loc[data['info'].isnull()].index)

    for criterion in null_criterion_list:
        idx_list = list(data.loc[data['info'] == criterion].index)
        null_idx_list.extend(idx_list)

    df_chill_days = data.loc[null_idx_list, :]

    df_work_days = data.drop(index=df_chill_days.index).reset_index(drop=True)
    df_work_days.loc[:, 'start_time'] = df_work_days.loc[df_work_days['start_time'].notna(), 'start_time'].apply(
        lambda x: str(x).split())
    df_work_days.loc[:, 'end_time'] = df_work_days.loc[df_work_days['end_time'].notna(), 'end_time'].apply(
        lambda x: str(x).split())

    # df_chill_days.to_csv('data_vault/total_data/df_chill_days.csv')
    # df_work_days.to_csv('data/total_data/1_prepared.csv')

    return df_work_days


def object_names_to_list(data):
    ''' Формируем список всех уникальных объектов из собранных данных

    :param data: pandas dataframe, содержащий все заявки с указанием наименований объектов
    :return: pandas dataframe + .csv файл
    '''

    obj_list = list()
    data['object'].apply(lambda x: obj_list.append(str(x).strip()) if str(x).strip() not in ('nan', '', '\n') else None)

    df_objects = pd.DataFrame({'object_name': list(set(obj_list))})

    # df_objects.to_csv('data/total_data/obj_unique_from_data.csv')

    return df_objects


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        # total_table_file = pd.read_csv('data/total_data/csv/0_raw_data.csv', index_col=0)
        # after_knn_file = pd.read_csv('data/total_data/csv/2_after_knn.csv', index_col=0)
        total = pd.read_csv('data_vault/total_data/0_raw_data.csv', index_col=0)

    main_preparation(total)
    # object_names_to_list(after_knn_file)

    return


if __name__ == '__main__':
    main()
