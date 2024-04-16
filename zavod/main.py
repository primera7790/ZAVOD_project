import warnings
from pathlib import Path

import pandas as pd

import data_mining
import data_preparation
import kNN_optimized
import hide_correction
import feature_engineering
import decision_tree


def all_in(obj_names_data, obj_features, requesters_data):
    """ Весь процесс, последовательно, от сбора данных до финальной аналитики

    :param obj_names_data: pandas dataframe, названия объектов на заводе
    :param obj_features: pandas dataframe, признаки для разбиения названий объектов
    :param requesters_data: pandas dataframe, список возможных заявителей
    :return: .csv файл
    """

    ''' ОПРЕДЕЛЕНИЕ СТРУКТУРы
    '''
    df_total = pd.DataFrame(columns=['date_day', 'date_night', 'object', 'installation', 'start_time', 'end_time',
                                     'master_day', 'master_night', 'info', 'requester', 'max_power', 'min_power',
                                     'power_per_24_hours', 'power_supply_scheme', 'file_name'])
    print('1. СБОР ДАННЫХ')

    ''' СБОР ДАННЫХ
    '''
    excel_dir = Path(Path(__file__).parent, 'data/excel_dir')

    prod_data_table = data_mining.data_mining(df_total, excel_dir)
    print('2. ОБРАБОТКА И НОРМАЛИЗАЦИЯ ДАННЫХ')

    ''' ОБРАБОТКА И НОРМАЛИЗАЦИЯ ДАННЫХ
    '''
    prepared_data = data_preparation.main_preparation(prod_data_table)
    print('3. ВЫЯВЛЯЕМ ЗАЯВИТЕЛЕЙ')

    ''' ВЫЯВЛЯЕМ ЗАЯВИТЕЛЯ 
    Используем kNN - метод ближайшего соседа
    '''
    after_knn_data = kNN_optimized.knn_algo(prepared_data, requesters_data)
    print('4. КОРРЕКТИРОВКА ДАННЫХ')

    ''' КОРРЕКТИРОВКА ДАННЫХ
    Легкие правки (файл скрыт по причине наличия персональных данных)
    '''
    after_knn_data = hide_correction.hide_correction(after_knn_data)

    print('5. ПОДГОТОВКА ДАННЫХ ДЛЯ АЛГОРИТМА ДЕРЕВА РЕШЕНИЙ')

    ''' ПОДГОТОВКА ДАННЫХ ДЛЯ АЛГОРИТМА ДЕРЕВА РЕШЕНИЙ
    Разделяем текст имени объектов, избавляемся от неинформативных элементов
    '''
    # obj_names_from_prod = obj_unique_from_data
    obj_names_from_prod = pd.DataFrame({'object_name': after_knn_data['object']})

    train_split_data = feature_engineering.to_objects_split(obj_names_data, train=True)
    train_split_data.index = train_split_data['idx']

    prod_split_data = feature_engineering.to_objects_split(obj_names_from_prod, prod=True)
    prod_split_data.index = prod_split_data['idx']

    # prod_split_data_unique = feature_engineering.to_objects_split(obj_names_from_prod, prod=True)  # опционально
    # prod_split_data_unique.index = prod_split_data_unique['idx']
    print('6. ПЕРЕВОД ИМЕН ОБЪЕКТОВ В ПРИЗНАКОВОЕ ПРОСТРАНСТВО')

    ''' ПЕРЕВОД ИМЕН ОБЪЕКТОВ В ПРИЗНАКОВОЕ ПРОСТРАНСТВО
    '''
    feature_train_data = feature_engineering.feature_engineering(train_split_data, obj_features, train=True)
    feature_train_data.index = feature_train_data['idx']
    del feature_train_data['idx']

    feature_prod_data = feature_engineering.feature_engineering(prod_split_data, obj_features, prod=True)
    feature_prod_data.index = feature_prod_data['idx']
    del feature_prod_data['idx']
    print('7. КЛАССИФИКАЦИЯ ОБЪЕКТОВ ПО ПРОИЗВОДСТВАМ')

    ''' КЛАССИФИКАЦИЯ ОБЪЕКТОВ ПО ПРОИЗВОДСТВАМ
    Используем Decision tree
    '''
    targets_data = train_split_data.loc[:, ['manufacture']]

    dt_predictions_data = decision_tree.decision_tree(feature_train_data, targets_data, feature_prod_data, obj_names_from_prod)

    prod_data = after_knn_data
    prod_data['manufacture'] = dt_predictions_data['prediction']

    ''' ФИНАЛЬНЫЕ ШТРИХИ
    '''
    prod_data = prod_data.loc[:, ['date_day', 'date_night', 'object', 'installation', 'manufacture', 'requester',
                                  'start_time', 'end_time', 'info', 'master_day', 'master_night', 'max_power',
                                  'min_power', 'power_per_24_hours', 'power_supply_scheme', 'file_name']]

    prod_data.to_csv('data/total_data/total_data.csv')
    print('ГОТОВО')

    return


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')

        obj_names_data = pd.read_csv('data/total_data/csv/obj_names.csv', index_col=0)
        obj_features = pd.read_csv('data/total_data/csv/obj_features.csv', index_col=0, header=None)
        requesters_data = pd.read_csv('data/total_data/csv/requesters.csv')

        # after_knn_file = pd.read_csv('data/total_data/csv/2_after_knn.csv', index_col=0)
        # obj_unique_from_data = pd.read_csv('data/total_data/csv/obj_unique_from_data.csv', index_col=0)

    all_in(obj_names_data, obj_features, requesters_data)

    return


if __name__ == '__main__':
    main()