import warnings

import pandas as pd


def masters_correction(file):
    """ Вносим лёгкие коррективы по в имена мастеров

    :param file: pandas dataframe
    :return: pandas dataframe
    """

    # данные скрыты во избежание засвета персональных данных

    return file


def requesters_correction(file):
    """ Вносим лёгкие коррективы по в имена заявителей

    :param file: pandas dataframe
    :return: pandas dataframe
    """

    # данные скрыты во избежание засвета персональных данных

    return file


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        raw_file = pd.read_csv('data_vault/total_data/csv/0_raw_data.csv', index_col=0)
        file = pd.read_csv('data_vault/total_data/csv/2_after_knn.csv', index_col=0)
        file2 = pd.read_csv('data_vault/total_data/csv/requesters.csv', index_col=0)

    masters_correction(raw_file)
    # requesters_correction(file)


if __name__ == '__main__':
    main()