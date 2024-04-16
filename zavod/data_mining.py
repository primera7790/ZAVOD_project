import os
import warnings
from pathlib import Path

import re
import math
import pandas as pd
from tqdm.auto import tqdm


def data_filter(dirty_data: list, date_name=False, time=False):
    '''Приведение данных к общему виду

    :param dirty_data: list, содержащий ненормированные данные
    :param date_name: bool, если dirty_data имеет вид [дата, [мастера,]]
    :param time: bool, если dirty_data имеет вид [время,]
    :return: list, содержащий нормированные данные
    '''

    filtered_data = dirty_data.copy()
    if date_name is True:
        filtered_data[0] = filtered_data[0] if filtered_data[0][-1] != '.' else filtered_data[0][:-1]
        filtered_data[0] = filtered_data[0] if filtered_data[0][0] not in ['.', '-'] else filtered_data[0][1:]

        filtered_data[1] = [m[:-3] + m[-3:].replace(' ', '') + '.' for m in filtered_data[1]]

    elif time is True:
        find_time = re.findall('\d+:\d+|\d+-\d+', str(filtered_data[0]))
        filtered_data = [pd.to_datetime(t.replace('-', ':'), format='%H:%M').time() for t in find_time]
        filtered_data = '\n'.join([str(o)[:5] for o in filtered_data])

    return filtered_data


def change_power_data(table, row_idx, col_idx):
    '''Адресный сбор данных по мощности из таблицы

    :param table: pandas dataframe, данные с файла
    :param row_idx: int, индекс строки
    :param col_idx: int, индекс колонки
    :return: list, список из четырех элементов
    '''

    max_p = pd.NA if type(table.iloc[row_idx, col_idx]) is str or math.isnan(table.iloc[row_idx, col_idx]) \
        else int(table.iloc[row_idx, col_idx])
    min_p = pd.NA if type(table.iloc[row_idx + 1, col_idx]) is str or math.isnan(table.iloc[row_idx + 1, col_idx]) \
        else int(table.iloc[row_idx + 1, col_idx])
    day = pd.NA if type(table.iloc[row_idx + 2, col_idx]) is str or math.isnan(table.iloc[row_idx + 2, col_idx]) \
        else int(table.iloc[row_idx + 2, col_idx])
    scheme = table.iloc[row_idx + 3, 1]

    return [max_p, min_p, day, scheme]


def data_normalize(data_before_norm: list):
    '''Приведение значения года в общей дате к виду 'YYYY', в частности '20..'

    :param data_before_norm: list, список вида [день, месяц, год]
    :return: list, список с корректными данными
    '''

    y = data_before_norm.copy()
    if len(y[2]) == 2:
        y[2] = '20' + y[2]

    return y


def data_mining(total_data, dir_path):
    ''' Сбор и компоновка данных из excel-таблиц, конвертированных из word-документов

    :param total_data: pandas dataframe, подготовленный для сбора данных
    :param dir_path: path, содержащий путь к директории с .xlsx файлами
    :return: pandas dataframe
    '''

    '''
    
    > Пофайловый сбор информации
    
    '''

    names_in_dir = os.listdir(dir_path)
    for name in tqdm(names_in_dir):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            file = pd.read_excel(str(dir_path) + f'/{name}', header=None)

        max_power = min_power = power_per_24_hours = power_supply_scheme = date \
            = date_day = date_night = master_day = master_night = pd.NA

        power_line_num = int()
        count_line = 0
        count_col = 0
        indicator = 0
        first_check = 0

        '''
        
        > Построчный сбор информации
        
        '''
        for line in file.values:
            base_line = str(line[0])
            '''
            
            - max_power 
            - min_power 
            - power_per_24_hours 
            - power_supply_scheme
            
            '''
            if 'мощность max' in base_line:
                power_line_num = count_line
                for c in file.values[count_line]:

                    if type(c) is str or type(c) is int:
                        try:
                            for i in range(3):
                                norm_value = str(file.iloc[power_line_num + i, count_col]).replace(',', '.').replace(' ', '')
                                file.iloc[power_line_num + i, count_col] = int(float(norm_value))

                            c_norm = str(c).replace(',', '.').replace(' ', '')
                            c = int(float(c_norm))

                        except ValueError:
                            pass

                    if type(c) is not int and count_col < len(file.columns) - 1:
                        count_col += 1
                    elif count_col == len(file.columns) - 1:
                        count_col = 2
                    else:
                        break

                power_data = change_power_data(file, power_line_num, count_col)
                max_power, min_power, power_per_24_hours, power_supply_scheme = power_data

                len_idx = len(total_data.index) - 1
                if first_check == 1:
                    total_data.iloc[len_idx, 10] = max_power
                    total_data.iloc[len_idx, 11] = min_power
                    total_data.iloc[len_idx, 12] = power_per_24_hours
                    total_data.iloc[len_idx, 13] = power_supply_scheme
            '''
            
            - date_day
            - date_night
            - master_day
            - master_night
            
            - *max_power
            - *min_power 
            - *power_per_24_hours 
            - *power_supply_scheme
            
            * - в случае наличия более актуальных данных
            
            '''
            if 'Сменный мастер' in base_line:
                line_without_whitespace = base_line.replace(' ', '')

                re_date = re.findall(r'[\d.–-]+', line_without_whitespace)[0]
                re_master_name = re.findall(r'\w[А-Яа-я]+ \w\.\w|\w[А-Яа-я]+ \w\. \w', base_line)

                if date is not pd.NA:
                    count_col += 1
                    first_check = 0

                    power_data = change_power_data(file, power_line_num, count_col)
                    max_power, min_power, power_per_24_hours, power_supply_scheme = power_data

                else:
                    first_check = 1

                date, master_name = data_filter([re_date, re_master_name], date_name=True)

                if len(master_name) == 2:
                    master_day = master_name[0]
                    master_night = master_name[1]
                elif len(master_name) == 1:
                    master_day = master_name[0]
                    master_night = ''

                date_split = date.split('-')
                date1_pre = date_split[0]
                date1_split = [d1 for d1 in date1_pre.split('.') if d1]
                date2_before_norm = date_split[1] if len(date_split) == 2 else pd.NA

                if date2_before_norm is pd.NA:
                    date1_norm = '.'.join(data_normalize(date1_split))
                    date_day = pd.to_datetime(date1_norm, format='%d.%m.%Y')
                    date_night = date_day

                else:
                    date2_split = [d2 for d2 in date2_before_norm.split('.') if d2]

                    if len(date1_split) == 1:
                        date1_split.append(date2_split[1])
                        date1_split.append(date2_split[2])
                    elif len(date1_split) == 2:
                        date1_split.append(date2_split[2])

                    date1_norm = '.'.join(data_normalize(date1_split))
                    date2_norm = '.'.join(data_normalize(date2_split))

                    date_day = pd.to_datetime(date1_norm, format='%d.%m.%Y')
                    date_night = pd.to_datetime(date2_norm, format='%d.%m.%Y')

                    if date_day > date_night:
                        date_day, date_night = date_night, date_day

                total_data.loc[len(total_data.index)] = [
                    date_day, date_night, '', '', '', '', master_day, master_night, '', '', max_power,
                    min_power, power_per_24_hours, power_supply_scheme, name
                ]

                indicator = 0
            '''
            
            - object_name
            - installation_name
            - start_time
            - end_time
            - info
            
            '''

            if line[0] in range(100) and line[5] not in range(10):
                object_name = line[1]
                installation_name = line[2]
                start_time = data_filter([line[3]], time=True)
                end_time = data_filter([line[4]], time=True)
                info = line[5]

                total_idx = len(total_data.index)
                if indicator == 0:
                    total_idx = len(total_data.index) - 1

                total_data.loc[total_idx] = [
                    date_day, date_night, object_name, installation_name, start_time, end_time, master_day,
                    master_night, info, '', max_power, min_power, power_per_24_hours, power_supply_scheme, name
                ]
                indicator = 1

            if 'тказов в работе' in str(line[5]):
                total_data.iloc[len(total_data.index) - 1, 8] = 'отказов в работе электрооборудования и электроснабжения не было'

            count_line += 1

    # total_data.to_csv('data/total_data/0_raw_data.csv')

    return total_data


def main():
    excel_dir = Path(Path(__file__).parent, 'data/excel_dir')

    df_total = pd.DataFrame(columns=['date_day', 'date_night', 'object', 'installation', 'start_time', 'end_time',
                                     'master_day', 'master_night', 'info', 'requester', 'max_power', 'min_power',
                                     'power_per_24_hours', 'power_supply_scheme', 'file_name'])

    data_mining(df_total, excel_dir)

    return


if __name__ == '__main__':
    main()
