# Порядок исполнения и описание

### Изначальные данные имеют следующий вид:
<p>
  <img width='400px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/word_table.PNG' alt='word_table'/>
  <img width='400px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/word_table_2.PNG' alt='word_table_2'/>
</p>

### Сторонними методами конвертируем в файлы формата .xlsx, после чего можно приступать.

## 1. Сбор данных
Файл: [data_mining.py](https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data_mining.py)
- Алгоритм проходится по каждому файлу отдельно и по ключевым закономерностям идентифицирует информацию;
- Найденные данные проходят первичную нормировку (обший формат даты, времени, фамилий с инициалами и т.д.);
- По возможности производим деление на логические блоки, формируя новые колонки.
  
#### Структура полученной таблицы:
<p>
  <img width='400px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/raw_data_info.PNG' alt='raw_data_info'/>
</p>
p.s. колонка "requester" на данном этапе остается пустой.

## 2. Подготовка данных
Файл: [data_preparation.py](https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data_preparation.py)
- Находим аномальные и некорректные значения, исправляем;
- Избавляемся от строк не содержащих полезной инормации (условно пустых);
- Приводим имеющиеся данные к конечному виду.

## 3. Формируем колонку "requester" при помощи метода **kNN**
Файл: [kNN_optimized.py](https://github.com/primera7790/ZAVOD_project/blob/master/zavod/kNN_optimized.py)
- Используем **kNN**, метод ближайшего соседа:
  - Формируем список возможных заявителей (тут пришлось вручную потрудиться);
  - Задаем алгоритм подсчета максимального количества буквенных комбинаций (поле для экспериментов);
  - Применяем алгоритм к текстовой колонке "info", для каждой строки присваиваем заявителя из соответствующего списка;
- Во избежание определения ложных фамилий, появляющихся в тексте после указания искомой, ограничил количество символов в зависимости от исходного размера;
- Также в директории "archive" сохранен файл с первоначальным вариантом исполнения. В дальнейшем, переписав код, удалось сократить время исполнения примерно в 20 раз.
  
#### Схематичная работа kNN:
<p>
  <img width='800px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/knn.PNG' alt='knn'/>
</p>

## 4. Корректировка данных
Файл: [hide_correction.py](https://github.com/primera7790/ZAVOD_project/blob/master/zavod/hide_correction.py)
#### Остается ряд проблемных мест, которые приходится решать "заплатками":
- фамилии часто указываются без инициалов, что поднимает проблему однофамильцев;
- ошибки в написании фамилий (если для колонки "requester" и kNN в частности это не является особой проблемой, то для колонок "master_day" и "master_night" это критично,
т.к. заполняем мы их непосредственно из исходной таблицы еще на стадии сбора данных.
#### Выявляем огрехи и правим, где-то точечно, где-то по закономерностям.

## 5. Формируем колонку "manufacture" при помощи алгоритма **Decision Tree**

### 5.1. Подготавливаем данные
Файл: [feature_engineering.py](https://github.com/primera7790/ZAVOD_project/blob/master/zavod/feature_engineering.py)
- Составляем:
   - список целевых признаков, т.е. всех производств на заводе;
   - [список признаков, описывающих каждый объект](https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/total_data/obj_features.csv);
   - перечень известных наименований объектов;
- Формируем таблицу объект-признак с целевыми значениями (для обучения модели):
  - Отсекаем лишние повторяющиеся приписки (вроде об., отд.);
    <p>
      <img width='130px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/obj_name_full.PNG' alt='obj_name_full'/>
    </p>
  
   - Присваиваем каждому объекту соответствующее ему производство (задаем целевой признак);
   - Сплитуем текст объектов по пробелу;
     <p>
       <img width='150px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/obj_name_split.PNG' alt='obj_name_split'/>
     </p>
    
   - Cоставляем перечень получившихся элементов списка с сохранением привязки к производству;
   - Переводим получившиевся данные в признаковое пространство
     <p>
       <img width='600px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/obj_name_split_features.PNG' alt='obj_name_split_features'/>
     </p>
    
- Составляем перечень уникальных записей в колонке "object";
- Формируем таблицу объект-признак по каждому объекту из табличных данных (для дальнейшего предсказания производств).
  
### 5.2. Классифицируем объекты по производствам
Файл: [decision_tree.py](https://github.com/primera7790/ZAVOD_project/blob/master/zavod/decision_tree.py)
- Используем Decision Tree, алгоритм дерева решений:
  - Обучаем модель на данных из таблицы объект-признак с целевыми значениями (удостоверившись в достаточности и объективности признаков);
  - Определяем к кому производству относится каждый из объектов таблицы для предсказания;
    <p>
      <img width='1000px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/obj_name_split_dirty_proba.PNG' alt='obj_name_split_dirty_proba'/>
    </p>
    
- Складываем вероятности отнесения к каждому из классов внутри каждого из объектов (напомню, мы их сплитовали);
  <p>
    <img width='1000px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/obj_name_full_total_proba.PNG' alt='obj_name_full_total_proba'/>
  </p>
  <p>
    <img width='400px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/obj_name_full_total_prediction.PNG' alt='obj_name_full_total_prediction'/>
  </p>
  
- Вносим корректировки, позволяющие избежать неправильного определения при паритете нескольких классов;
  
  #### Оценка значимости признаков полученной модели:
  <p>
    <img width='400px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/feature_importance.png' alt='feature_importance'/>
  </p>

 - Сохраняем полученные предсказания в колонку "manufacture" итоговой таблицы.
   
   #### Структура итоговой таблицы:
   <p>
     <img width='400px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/total_data_info.PNG' alt='total_data_info'/>
   </p>
 
## 6. Анализ данных и визуализация
Файл: [analytics.py](https://github.com/primera7790/ZAVOD_project/blob/master/zavod/analytics.py) <br>
Содержит, в основном, закомментированные нагромождения независимых запросов
#### [Результаты запросов сведены в ознокомительный .pdf файл](https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BD%D0%B0%D0%B1%D0%BB%D1%8E%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F.pdf)
P.S. С целью сохранения персональной информации и коммерческих данных часть информации скрыта. Презентация носит учебный ознакомительный характер и является демонстрацией визуального отображения собранных, предсказанных и агрегированных данных.


## 7. ALL IN
Файл: [main.py](https://github.com/primera7790/ZAVOD_project/blob/master/zavod/main.py) <br>
Содержит инструкции последовательной инициализации всех вышеописанных процессов
<p>
  <img width='400px' src='https://github.com/primera7790/ZAVOD_project/blob/master/zavod/data/images/main_process.PNG' alt='main_process'/>
</p>

