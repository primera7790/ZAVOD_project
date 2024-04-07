import warnings

import numpy as np
import pandas as pd
from tqdm.auto import tqdm


def comparing(text, target_name):
    max_combo = 0
    count_step = 0
    count_hit = 0

    for l_info_idx in range(len(text)):

        letter_info = text[l_info_idx]
        letter_target = target_name[count_step]

        if letter_info == letter_target:

            for l_combo_idx in range(l_info_idx, len(text)):

                if text[l_combo_idx] == target_name[count_step]:
                    count_hit += 1

                    max_combo = max(max_combo, count_hit)
                else:
                    count_hit = 0
                    count_step = 0
                    break

                if count_step < len(target_name) - 1:
                    count_step += 1
                else:
                    count_hit = 0
                    count_step = 0
                    break
        else:
            if max_combo >= 5:
                break

    return max_combo if max_combo >= 4 else 0


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        data_file = pd.read_csv('data/total_data/csv/1_prepared.csv', index_col=0)
        requesters_file = pd.read_csv('data/total_data/csv/requesters.csv')

    info_data = data_file['info'].apply(lambda x: x[:90] if len(x) > 100 else x[:50])
    targets_data = requesters_file['requester_name']

    targets_data_edit = targets_data.copy()
    targets_data_edit[0] = 'Й'

    predictions_idx = info_data.apply(
        lambda x: np.argmax(
            targets_data_edit.apply(
                lambda y: np.max(
                    comparing(x, y)))))

    data_file['requester'] = predictions_idx.apply(lambda x: targets_data[x])

    data_file.to_csv('data/total_data/2_after_knn.csv')

    return


if __name__ == '__main__':
    main()