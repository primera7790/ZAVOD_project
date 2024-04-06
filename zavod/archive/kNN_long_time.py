import warnings

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    data_file = pd.read_csv('../data/total_data/csv/1_preparationed.csv', index_col=0)
    requesters_file = pd.read_csv('../data/total_data/csv/requesters.csv')


info_data = data_file['info'].apply(lambda x: x[:90] if len(x) > 100 else x[:50])
targets_data = requesters_file['requester_name']

info_data_letter_quan_array = info_data.apply(lambda x: len(x)).to_numpy()
targets_letter_quan_array = targets_data.apply(lambda x: len(x)).to_numpy()

distance_matrix = np.zeros([len(targets_data), len(info_data)])

targets_data_edit = targets_data.copy()
targets_data_edit[0] = 'Й'

for target_idx in tqdm(range(len(targets_data))):
    for info_idx in range(len(info_data)):

        max_combo = 0
        count_step = 0
        count_hit = 0

        for l_info_idx in range(info_data_letter_quan_array[info_idx]):

            text_info = info_data[info_idx]
            text_target = targets_data_edit[target_idx]
            letter_info = text_info[l_info_idx]
            letter_target = text_target[count_step]

            if letter_info == letter_target:

                for l_combo_ibx in range(l_info_idx, info_data_letter_quan_array[info_idx]):

                    if text_info[l_combo_ibx] == text_target[count_step]:
                        count_hit += 1

                        max_combo = max(max_combo, count_hit)
                    else:
                        count_hit = 0
                        count_step = 0
                        break

                    if count_step < len(text_target) - 1:
                        count_step += 1
                    else:
                        count_hit = 0
                        count_step = 0
                        break
            else:
                if max_combo >= 5:
                    break

        distance_matrix[target_idx, info_idx] = max_combo if max_combo >= 4 else 0

prediction_values = np.max(distance_matrix, axis=0)
predictions = np.argmax(distance_matrix, axis=0)

names = requesters_file.loc[predictions, 'requester_name'].reset_index(drop=True)
data_file['requester'] = names

data_file.to_csv('data/total_data/2_after_knn1.csv')