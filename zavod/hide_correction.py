import os
import sys
import warnings
from pathlib import Path

import re
import math
import numpy as np
import pandas as pd
from tqdm.auto import tqdm


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        file = pd.read_csv('data/total_data/csv/2_after_knn.csv', index_col=0)
        file2 = pd.read_csv('data/total_data/csv/requesters.csv', index_col=0)

    file.loc[file['requester'] == 'Даутов Р.Р.', 'requester'] = 'Даутов Р.C.'
    file.loc[1250, 'requester'] = 'Даутов Р.Р.'

    file.loc[file['requester'] == 'Иванов Д.С.', 'requester'] = 'Иванов Д.Н.'
    file.loc[file['requester'] == 'Иванов', 'requester'] = 'Иванов Д.Н.'
    file.loc[[498, 1167], 'requester'] = 'Иванов Д.С.'
    file.loc[[1634, 3220], 'requester'] = 'Иванов'

    file.loc[file['requester'] == 'Мухамадеев Д.Х.', 'requester'] = 'Мухамадеев И.Н.'
    file.loc[file['requester'] == 'Мухамадеев', 'requester'] = 'Мухамадеев И.Н.'
    file.loc[[740, 890, ], 'requester'] = 'Мухамадеев Д.Х.'
    file.loc[[1883, 2548, ], 'requester'] = 'Мухамадеев'

    file.loc[file['requester'] == 'Петров И.А.', 'requester'] = 'Петров Э.В.'
    file.loc[[305, 2589, ], 'requester'] = 'Петров И.А.'

    file.loc[file['requester'] == 'Федоров В.А.', 'requester'] = 'Фёдоров Д.В.'
    file.loc[file['requester'] == 'Фёдоров В.А.', 'requester'] = 'Фёдоров Д.В.'
    file.loc[file['requester'] == 'Федоров Д.В.', 'requester'] = 'Фёдоров Д.В.'
    file.loc[[199, 716, 3692], 'requester'] = 'Фёдоров В.А.'

    file.loc[file['requester'] == 'Хазиев И.И.', 'requester'] = 'Хазиев И.Ф.'
    file.loc[file['requester'] == 'Хазиев', 'requester'] = 'Хазиев И.Ф.'
    file.loc[815, 'requester'] = 'Хазиев И.И.'
    file.loc[1137, 'requester'] = 'Хазиев'

    file.loc[file['requester'] == 'Хасанов Д.Г.', 'requester'] = 'Хасанов'
    file.loc[file['requester'] == 'Хасанов М.Ш.', 'requester'] = 'Хасанов'
    file.loc[file['requester'] == 'Хасанов Д.Р.', 'requester'] = 'Хасанов'
    file.loc[1479, 'requester'] = 'Хасанов Д.Г.'
    file.loc[[195, 316, 3606], 'requester'] = 'Хасанов М.Ш.'
    file.loc[[84, 208, 219, 448, 449, 554, 938, 1213, 1925, 2109, 2513, 3700], 'requester'] = 'Хасанов Д.Р.'
    file.loc[2636, 'requester'] = 'Боев А.И.'
    file.loc[3414, 'requester'] = 'Котяшов'

    file.to_csv('data/total_data/csv/2_after_knn.csv')



if __name__ == '__main__':
    main()