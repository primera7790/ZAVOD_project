import warnings

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    data_file = pd.read_csv('data/total_data/csv/1_preparationed.csv', index_col=0)
    data_file.loc[:, 'requester'] = data_file.loc[:, 'requester'].astype(str)
    requesters_file = pd.read_csv('data/total_data/csv/requesters.csv')


info_data = data_file['info'].apply(lambda x: x[:90])
targets_data = requesters_file['requester_name']
surname_data = targets_data.apply(lambda x: x.split(' ')[0][:-1] if x.split(' ')[0][-1] == 'а' else x.split(' ')[0])
# predict_surname_list =

sur = surname_data[1:]
for info_idx in tqdm(range(len(info_data))):
    # print(info_idx)
    # print(info_data[info_idx])
    sur_filter = sur.apply(lambda x: x if x in info_data[info_idx] else pd.NA)
    notna_sur = sur_filter[sur_filter.notna()]
    # print('here')
    data_file.loc[info_idx, 'requester'] = targets_data[notna_sur.index[0]] if len(notna_sur) > 0 else 'не указан'
    # print(targets_data[notna_sur.index[0]])
    # sur = sur.notna()
    # print(sur[info_idx])

    # print('yes' if sur[info_idx] in info_data[info_idx] else 'no')
    # break
data_file.to_csv('data/total_data/check.csv')

# surname_data.to_csv('data/total_data/check.csv')



#
# data_file['requester'].apply(lambda x: )
#
#
#
# # info_data_letter_quan_array = info_data.apply(lambda x: len(x)).to_numpy()
# # targets_letter_quan_array = targets_data.apply(lambda x: len(x)).to_numpy()
# #
# # distance_matrix = np.zeros([len(targets_data), len(info_data)])
#
# for target_idx in tqdm(range(len(targets_data))):
#     for info_idx in range(len(info_data)):
#
#         max_combo = 0
#         count_step = 0
#         count_hit = 0
#
#         for l_info_idx in range(info_data_letter_quan_array[info_idx]):
#
#             text_info = info_data[info_idx]
#             text_target = targets_data[target_idx]
#             letter_info = text_info[l_info_idx]
#             letter_target = text_target[count_step]
#
#             if letter_info == letter_target:
#
#                 for l_combo_ibx in range(l_info_idx, info_data_letter_quan_array[info_idx]):
#
#                     if text_info[l_combo_ibx] == text_target[count_step]:
#                         count_hit += 1
#
#                         max_combo = max(max_combo, count_hit)
#                     else:
#                         count_hit = 0
#                         count_step = 0
#                         break
#
#                     if count_step < len(text_target) - 1:
#                         count_step += 1
#                     else:
#                         count_hit = 0
#                         count_step = 0
#                         break
#             else:
#                 if max_combo >= 5:
#                     break
#
#         distance_matrix[target_idx, info_idx] = max_combo if max_combo >= 4 else 0
#
# prediction_values = np.max(distance_matrix, axis=0)
# predictions = np.argmax(distance_matrix, axis=0)
#
# names = requesters_file.loc[predictions, 'requester_name'].reset_index(drop=True)
# data_file['requester'] = names
#
# data_file.to_csv('data/total_data/2_after_knn.csv')
