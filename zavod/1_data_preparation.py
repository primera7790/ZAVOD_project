import warnings

import pandas as pd


def main():
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
    df_work_days.loc[:, 'start_time'] = df_work_days.loc[df_work_days['start_time'].notna(), 'start_time'].apply(
        lambda x: str(x).split())
    df_work_days.loc[:, 'end_time'] = df_work_days.loc[df_work_days['end_time'].notna(), 'end_time'].apply(
        lambda x: str(x).split())

    df_work_days.to_csv('data/total_data/1_prepared.csv')
    return


if __name__ == '__main__':
    main()