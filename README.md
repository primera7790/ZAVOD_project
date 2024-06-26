# Pet-project на реальных данных

## Технологи
- Язык: &nbsp; `python` ;
- Библиотеки: &nbsp; `pandas` , `numpy` , `sklearn` , `matplotlib` ;
- ML-алгоритмы: &nbsp; `kNN` , `Decision Tree` .
  
## Описание
&nbsp; &nbsp; Программа преобразует множество excel-файлов (с вручную записанными данными) в единую csv-таблицу.<br>
&nbsp; &nbsp; Подготовливает данные (извлекает, нормирует, обеспечевает достаточность).<br>
&nbsp; &nbsp; На основе полученных данных производится их агрегация, аналитика и визуализация.

## Основные процессы
- сбор данных;
- обработка;
- структурирование;
- классифицирование по наибольшему подобию, применяя метод ___kNN___;
- перевод определенных данных в признаковое пространство и дальнейшая классификация при помощи ___Decision Tree___ модели;
- агрегация, аналитика и визуализация (формирование презентации).
  
### Более подробное описание исполнения всех процессов:
- либо по данной ссылке: &nbsp; [ссылка](https://github.com/primera7790/ZAVOD_project/tree/master/zavod) ;
- либо в README.md файле директории "zavod".

## Важное дополнение
&nbsp; &nbsp; В проект добавлены демонстрационные данные.<br>
&nbsp; &nbsp; Во избежание разглашения персональных данных и закрытой информации, данные демонстрационных файлов были вольно изменены.<br>
&nbsp; &nbsp; Фамилии были сгенерированы случайно при помощи сервиса [randomus.ru](https://randomus.ru/). Все совпадения с реальными лицами случайны.

## Инструкция по запуску
1. Скачать/скопировать данные репозитория;
2. Установить зависимости, указанные в файле `requirements.txt` ;
3. Запустить файл `/zavod/main.py` .

Основные директории:
- Сырые данные: &nbsp; [/zavod/data/excel_dir/](https://github.com/primera7790/ZAVOD_project/tree/master/zavod/data/excel_dir);
- Данные для обучения моделей: &nbsp; [zavod/data/total_data/csv/](https://github.com/primera7790/ZAVOD_project/tree/master/zavod/data/total_data/csv);
- Итоговая таблица: [/zavod/data/total_data](https://github.com/primera7790/ZAVOD_project/tree/master/zavod/data/total_data).
